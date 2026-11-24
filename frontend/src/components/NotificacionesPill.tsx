import { useState, useEffect, useCallback } from "react";
import "./NotificacionesPill.css";
import { getStoredUser, getAuthToken, api } from "../services/api";

interface NotifItem {
  id: string | number;
  titulo: string;
  mensaje: string;
  fecha: string;
  leida: boolean;
  tipo: string;
  accionVista?: string;
  creado_en?: string;
}

interface NotificacionesPillProps {
  onNavigate?: (vista: string) => void;
}

const POLL_MS = 30_000; // polling cada 30 segundos

function formatFecha(raw: string | undefined): string {
  if (!raw) return "Ahora";
  try {
    const d = new Date(raw);
    const hoy = new Date();
    const ayer = new Date();
    ayer.setDate(hoy.getDate() - 1);
    if (d.toDateString() === hoy.toDateString()) {
      return `Hoy, ${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`;
    }
    if (d.toDateString() === ayer.toDateString()) {
      return `Ayer, ${d.getHours().toString().padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}`;
    }
    return d.toLocaleDateString("es-CO", { day: "2-digit", month: "short" });
  } catch {
    return raw;
  }
}

function NotificacionesPill({ onNavigate }: NotificacionesPillProps) {
  const [abierto, setAbierto]           = useState<boolean>(false);
  const [notificaciones, setNotifs]     = useState<NotifItem[]>([]);
  const [cargando, setCargando]         = useState<boolean>(false);
  const usuario = getStoredUser();
  const tieneToken = !!getAuthToken();

  // ── CARGA DESDE API ────────────────────────────────────────────
  const cargarDesdeApi = useCallback(async () => {
    if (!tieneToken || !usuario?.id) {
      setNotifs([]);
      return;
    }
    try {
      const res = await api.obtenerNotificaciones(false);
      if (res.success && Array.isArray(res.data)) {
        const mapeadas: NotifItem[] = res.data.map((n: any) => ({
          id: n.id,
          titulo: n.titulo,
          mensaje: n.mensaje,
          fecha: formatFecha(n.creado_en),
          leida: !!n.leida,
          tipo: n.tipo || "reserva",
          accionVista: n.tipo === "reserva" && usuario?.rol === "admin"
            ? "admin_dashboard"
            : "client_dashboard",
          creado_en: n.creado_en,
        }));
        setNotifs(mapeadas);
        return;
      }
    } catch {
      // fallback a localStorage si API no responde
    }
    cargarDesdeLocal();
  }, [tieneToken, usuario?.id, usuario?.rol]);

  // ── FALLBACK localStorage (estrictamente por usuario) ──────────
  const cargarDesdeLocal = useCallback(() => {
    if (!usuario?.id) {
      setNotifs([]);
      return;
    }
    const clave = usuario?.rol === "admin"
      ? "fz_notifs_admin"
      : `fz_notifs_${usuario.id}`;
    try {
      const raw = localStorage.getItem(clave);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setNotifs(parsed);
          return;
        }
      }
    } catch {}
    // Si no hay nada, lista vacía
    setNotifs([]);
  }, [usuario?.id, usuario?.rol]);

  // ── CARGA INICIAL + POLLING ────────────────────────────────────
  useEffect(() => {
    cargarDesdeApi();

    const handleEvento = () => cargarDesdeApi();
    window.addEventListener("fz_notification_update", handleEvento);
    window.addEventListener("storage", handleEvento);

    const intervalo = setInterval(cargarDesdeApi, POLL_MS);

    return () => {
      window.removeEventListener("fz_notification_update", handleEvento);
      window.removeEventListener("storage", handleEvento);
      clearInterval(intervalo);
    };
  }, [cargarDesdeApi]);

  // ── ACCIONES ───────────────────────────────────────────────────
  const marcarUnaLeida = async (notif: NotifItem) => {
    // Optimista: actualizar UI inmediatamente
    setNotifs((prev) => prev.map((n) => n.id === notif.id ? { ...n, leida: true } : n));

    // Intentar marcar en BD
    try {
      if (tieneToken && typeof notif.id === "number") {
        await api.marcarNotificacionLeida(notif.id as number);
      }
    } catch {}

    // También en localStorage (fallback)
    const clave = usuario?.rol === "admin"
      ? "fz_notifs_admin"
      : `fz_notifs_${usuario?.id || "guest"}`;
    try {
      const raw = localStorage.getItem(clave);
      if (raw) {
        const lista = JSON.parse(raw);
        const updated = lista.map((n: any) => n.id === notif.id ? { ...n, leida: true } : n);
        localStorage.setItem(clave, JSON.stringify(updated));
      }
    } catch {}

    setAbierto(false);
    if (notif.accionVista && onNavigate) {
      onNavigate(notif.accionVista);
    }
  };

  const marcarTodasLeidas = async () => {
    setNotifs((prev) => prev.map((n) => ({ ...n, leida: true })));
    try {
      if (tieneToken) await api.marcarTodasLeidas();
    } catch {}
    // localStorage
    const clave = usuario?.rol === "admin"
      ? "fz_notifs_admin"
      : `fz_notifs_${usuario?.id || "guest"}`;
    try {
      const raw = localStorage.getItem(clave);
      if (raw) {
        const lista = JSON.parse(raw);
        localStorage.setItem(clave, JSON.stringify(lista.map((n: any) => ({ ...n, leida: true }))));
      }
    } catch {}
    window.dispatchEvent(new Event("fz_notification_update"));
  };

  const limpiarNotificaciones = () => {
    setNotifs([]);
    const clave = usuario?.rol === "admin"
      ? "fz_notifs_admin"
      : `fz_notifs_${usuario?.id || "guest"}`;
    localStorage.removeItem(clave);
    window.dispatchEvent(new Event("fz_notification_update"));
  };

  if (!tieneToken || !usuario?.id) {
    return null;
  }

  const noLeidas = notificaciones.filter((n) => !n.leida).length;

  return (
    <div className="fz-notif-wrapper">
      <button
        type="button"
        className={`fz-btn-bell ${noLeidas > 0 ? "has-unread" : ""}`}
        onClick={() => { setAbierto(!abierto); if (!abierto) cargarDesdeApi(); }}
        title={`Notificaciones (${noLeidas} nuevas)`}
        aria-label="Notificaciones"
      >
        <span className="fz-bell-svg-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 0 1-3.46 0" />
          </svg>
        </span>
        {noLeidas > 0 && <span className="fz-bell-badge">{noLeidas}</span>}
      </button>

      {abierto && (
        <div className="fz-notif-dropdown">
          <div className="fz-notif-header">
            <div className="fz-notif-header-title">
              <h4>Centro de Notificaciones</h4>
              {noLeidas > 0 && <span className="fz-notif-unread-tag">{noLeidas} nuevas</span>}
            </div>
            <div className="fz-notif-header-actions">
              {noLeidas > 0 && (
                <button type="button" className="fz-btn-mark-all" onClick={marcarTodasLeidas}>
                  Marcar leídas
                </button>
              )}
              <button
                type="button"
                className="fz-btn-close-notif"
                onClick={() => setAbierto(false)}
                title="Cerrar panel"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="fz-notif-list">
            {notificaciones.length === 0 ? (
              <div className="fz-notif-empty">
                <p>No tienes notificaciones pendientes.</p>
                <small style={{ color: "#64748b", fontSize: "11px" }}>
                  {usuario?.rol === "admin"
                    ? "Las notificaciones aparecen aquí cuando los clientes realicen o cancelen reservas."
                    : "Las notificaciones aparecen aquí cuando el administrador gestione tus reservas."}
                </small>
              </div>
            ) : (
              notificaciones.map((n) => (
                <div
                  key={n.id}
                  className={`fz-notif-item ${n.leida ? "leida" : "unread"}`}
                  onClick={() => marcarUnaLeida(n)}
                >
                  <div className="fz-notif-item-top">
                    <span className={`fz-notif-type-tag ${n.tipo}`}>
                      {n.tipo === "reserva"  && "RESERVA"}
                      {n.tipo === "sistema"  && "SISTEMA"}
                      {n.tipo === "promocion" && "PROMOCIÓN"}
                      {n.tipo === "promo"    && "PROMOCIÓN"}
                      {n.tipo === "pago"     && "PAGO"}
                      {n.tipo === "seguridad" && "SEGURIDAD"}
                    </span>
                    <span className="fz-notif-time">{n.fecha}</span>
                  </div>
                  <strong className="fz-notif-item-title">{n.titulo}</strong>
                  <p className="fz-notif-item-msg">{n.mensaje}</p>
                </div>
              ))
            )}
          </div>

          {notificaciones.length > 0 && (
            <div className="fz-notif-footer">
              <button type="button" className="fz-btn-clear-notifs" onClick={limpiarNotificaciones}>
                Limpiar historial
              </button>
              <button type="button" className="fz-btn-clear-notifs" onClick={cargarDesdeApi}
                style={{ marginLeft: "8px", background: "#1e293b" }}>
                🔄 Actualizar
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default NotificacionesPill;
