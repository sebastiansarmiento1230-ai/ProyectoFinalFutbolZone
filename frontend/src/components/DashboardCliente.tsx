import { useState, useEffect, useRef, useMemo } from "react";
import "./DashboardCliente.css";
import * as XLSX from "xlsx";
import { api, setStoredUser } from "../services/api";
import { notificarAdmin, notificarCliente } from "../services/notifications";
import TicketReservaModal from "./TicketReservaModal";
import TorneosView from "./TorneosView";
import TablonRetos from "./TablonRetos";
import RecuperarPasswordModal from "./RecuperarPasswordModal";
import NotificacionesPill from "./NotificacionesPill";

interface DashboardClienteProps {
  usuario: any;
  onLogout: () => void;
  onGoToBooking: () => void;
}

function DashboardCliente({ usuario, onLogout, onGoToBooking }: DashboardClienteProps) {
  const [tabActiva, setTabActiva] = useState<"resumen" | "reservas" | "torneos" | "retos" | "perfil">("resumen");
  const [misReservas, setMisReservas] = useState<any[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [reservaParaTicket, setReservaParaTicket] = useState<any | null>(null);
  const [mensaje, setMensaje] = useState<string | null>(null);
  const [mostrarModalRecuperar, setMostrarModalRecuperar] = useState<boolean>(false);

  // 🔍 ESTADOS DE BÚSQUEDA Y FILTRADO DE RESERVAS (ETAPA 4)
  const [filtroCancha, setFiltroCancha] = useState<string>("todas");
  const [filtroFechaModo, setFiltroFechaModo] = useState<"todas" | "exacta" | "rango">("todas");
  const [fechaExacta, setFechaExacta] = useState<string>("");
  const [fechaDesde, setFechaDesde] = useState<string>("");
  const [fechaHasta, setFechaHasta] = useState<string>("");
  const [busquedaTexto, setBusquedaTexto] = useState<string>("");

  // Estados de edición de perfil
  const [nombre, setNombre] = useState<string>(usuario?.nombre || "");
  const [apellido, setApellido] = useState<string>(usuario?.apellido || "");
  const [telefono, setTelefono] = useState<string>(usuario?.telefono || "");
  const [guardandoPerfil, setGuardandoPerfil] = useState<boolean>(false);
  const [mensajePerfil, setMensajePerfil] = useState<{ texto: string; tipo: "exito" | "error" } | null>(null);

  // Foto de perfil / Avatar
  const [avatarUrl, setAvatarUrl] = useState<string>(() => {
    return localStorage.getItem(`fz_avatar_${usuario?.id}`) || "";
  });
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    cargarReservas();
  }, [usuario?.id]);

  const cargarReservas = async () => {
    setCargando(true);
    try {
      const res = await api.obtenerMisReservas();
      if (res.success && Array.isArray(res.data)) {
        setMisReservas(res.data);
      }
    } catch {
      setMisReservas([]);
    } finally {
      setCargando(false);
    }
  };

  const cancelarReserva = async (id: number) => {
    if (!confirm("¿Está seguro de que desea cancelar esta reserva?")) return;
    try {
      const resCancelada = misReservas.find((r) => r.id === id);
      await api.cancelarReserva(id);
      
      // Notificar al administrador
      notificarAdmin({
        titulo: "Reserva Cancelada por Cliente",
        mensaje: `${usuario?.nombre || "Un cliente"} ha cancelado su reserva en ${resCancelada?.cancha_nombre || "la cancha"} del ${resCancelada?.fecha || "la fecha agendada"}.`,
        tipo: "reserva",
        accionVista: "admin_dashboard",
      });

      // Notificar al cliente
      notificarCliente(usuario?.id, {
        titulo: "Turno Cancelado",
        mensaje: `Tu reserva #${id} ha sido cancelada correctamente y el horario quedó disponible.`,
        tipo: "reserva",
        accionVista: "client_dashboard",
      });

      setMensaje("Reserva cancelada con éxito.");
      cargarReservas();
      setTimeout(() => setMensaje(null), 3000);
    } catch (err: any) {
      alert("Error al cancelar reserva: " + err.message);
    }
  };

  // 🔍 Limpiar todos los filtros y restablecer el historial completo
  const limpiarFiltros = () => {
    setFiltroCancha("todas");
    setFiltroFechaModo("todas");
    setFechaExacta("");
    setFechaDesde("");
    setFechaHasta("");
    setBusquedaTexto("");
  };

  const hayFiltrosActivos =
    filtroCancha !== "todas" ||
    (filtroFechaModo === "exacta" && !!fechaExacta) ||
    (filtroFechaModo === "rango" && (!!fechaDesde || !!fechaHasta)) ||
    busquedaTexto.trim() !== "";

  // Conteo de reservas reales por cancha del usuario autenticado
  const conteoCanchas = useMemo(() => {
    let central = 0;
    let norte = 0;
    let sur = 0;
    misReservas.forEach((r) => {
      const nom = (r.cancha_nombre || "").toLowerCase();
      if (nom.includes("central")) central++;
      else if (nom.includes("norte")) norte++;
      else if (nom.includes("sur")) sur++;
    });
    return { central, norte, sur, total: misReservas.length };
  }, [misReservas]);

  // Filtrado reactivo sobre las reservas reales del usuario que inició sesión
  const misReservasFiltradas = useMemo(() => {
    return misReservas.filter((r) => {
      // 1. Filtro por cancha específica (Cancha Central, Cancha Norte, Cancha Sur)
      if (filtroCancha !== "todas") {
        const nom = (r.cancha_nombre || "").toLowerCase();
        const f = filtroCancha.toLowerCase();
        if (!nom.includes(f) && !f.includes(nom)) {
          return false;
        }
      }

      // 2. Filtro por fecha (Fecha específica o rango desde/hasta)
      if (filtroFechaModo === "exacta" && fechaExacta) {
        if (r.fecha !== fechaExacta) return false;
      } else if (filtroFechaModo === "rango") {
        if (fechaDesde && r.fecha < fechaDesde) return false;
        if (fechaHasta && r.fecha > fechaHasta) return false;
      }

      // 3. Barra de búsqueda por texto
      if (busquedaTexto.trim()) {
        const query = busquedaTexto.trim().toLowerCase();
        const coincideId = String(r.id).includes(query);
        const coincideCancha = (r.cancha_nombre || "").toLowerCase().includes(query);
        const coincideFecha = (r.fecha || "").includes(query);
        const coincideEstado = (r.estado || "").toLowerCase().includes(query);
        const coincideMetodo = (r.metodo_pago || "").toLowerCase().includes(query);
        if (!coincideId && !coincideCancha && !coincideFecha && !coincideEstado && !coincideMetodo) {
          return false;
        }
      }

      return true;
    });
  }, [misReservas, filtroCancha, filtroFechaModo, fechaExacta, fechaDesde, fechaHasta, busquedaTexto]);

  const exportarExcelMisReservas = () => {
    const listaAExportar = hayFiltrosActivos ? misReservasFiltradas : misReservas;
    if (listaAExportar.length === 0) {
      alert("No tienes reservas registradas para exportar con los filtros seleccionados.");
      return;
    }
    const dataFilas = listaAExportar.map((r) => {
      const metodo = r.metodo_pago || (r.notas?.includes("NEQUI") ? "Nequi" : r.notas?.includes("DAVIPLATA") ? "Daviplata" : r.notas?.includes("TARJETA") ? "Tarjeta" : "Efectivo");
      return {
        "ID": r.id,
        "Cancha": r.cancha_nombre || "Cancha Sintética",
        "Fecha": r.fecha,
        "Horario": `${r.hora_inicio.substring(0, 5)} - ${r.hora_fin.substring(0, 5)}`,
        "Total COP": Number(r.precio_total) || 50000,
        "Método de Pago": metodo,
        "Estado": r.estado?.toUpperCase(),
        "Detalles": r.notas || "Reserva estándar",
      };
    });

    const worksheet = XLSX.utils.json_to_sheet(dataFilas);
    worksheet["!cols"] = [
      { wch: 8 },
      { wch: 22 },
      { wch: 14 },
      { wch: 16 },
      { wch: 14 },
      { wch: 18 },
      { wch: 14 },
      { wch: 30 },
    ];
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Mis Reservas");
    const fechaHoy = new Date().toISOString().split("T")[0];
    XLSX.writeFile(workbook, `Historial_Reservas_${usuario?.nombre || "Cliente"}_${fechaHoy}.xlsx`);
  };

  const handleSubirFoto = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 2 * 1024 * 1024) {
      alert("La imagen es muy grande. Por favor sube una foto menor a 2MB.");
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      setAvatarUrl(base64);
      localStorage.setItem(`fz_avatar_${usuario?.id}`, base64);
      setMensajePerfil({ texto: "Foto de perfil actualizada correctamente.", tipo: "exito" });
      setTimeout(() => setMensajePerfil(null), 3000);
    };
    reader.readAsDataURL(file);
  };

  const eliminarFoto = () => {
    setAvatarUrl("");
    localStorage.removeItem(`fz_avatar_${usuario?.id}`);
    setMensajePerfil({ texto: "Foto de perfil restablecida.", tipo: "exito" });
    setTimeout(() => setMensajePerfil(null), 3000);
  };

  const guardarPerfil = async (e: React.FormEvent) => {
    e.preventDefault();
    setGuardandoPerfil(true);
    setMensajePerfil(null);

    try {
      const res = await api.actualizarPerfil(usuario.id, { nombre, apellido, telefono });
      if (res.success) {
        const usuarioActualizado = { ...usuario, nombre, apellido, telefono };
        setStoredUser(usuarioActualizado);
        notificarCliente(usuario?.id, {
          titulo: "Perfil y Datos Actualizados",
          mensaje: "Tus datos personales y número de contacto fueron guardados correctamente.",
          tipo: "seguridad",
          accionVista: "client_dashboard",
        });
        setMensajePerfil({ texto: "Perfil actualizado con éxito.", tipo: "exito" });
        setTimeout(() => setMensajePerfil(null), 3000);
      } else {
        setMensajePerfil({ texto: res.message || "Error al actualizar perfil", tipo: "error" });
      }
    } catch (err: any) {
      setMensajePerfil({ texto: err.message || "Error al conectar con el servidor", tipo: "error" });
    } finally {
      setGuardandoPerfil(false);
    }
  };

  // Cálculos de métricas reales (exclusivamente de este usuario)
  const reservasValidas = misReservas.filter((r) => r.estado === "confirmada" || r.estado === "completada");
  const totalInvertidoReal = reservasValidas.reduce((sum, r) => sum + (Number(r.precio_total) || 0), 0);
  const partidosJugadosReal = misReservas.filter((r) => r.estado === "completada").length;
  const reservasActivas = misReservas.filter((r) => r.estado === "confirmada" || r.estado === "pendiente");
  const totalReservasReal = misReservas.length;
  const pendientesReal = misReservas.filter((r) => r.estado === "pendiente").length;
  const confirmadasReal = misReservas.filter((r) => r.estado === "confirmada").length;
  const rechazadasReal = misReservas.filter((r) => r.estado === "rechazada").length;

  let rolBadge = "JUGADOR TITULAR";
  if (partidosJugadosReal >= 10) {
    rolBadge = "JUGADOR VIP";
  } else if (partidosJugadosReal >= 4) {
    rolBadge = "CAPITÁN";
  } else if (partidosJugadosReal === 0) {
    rolBadge = "JUGADOR DEBUTANTE";
  }

  const iniciales = `${usuario?.nombre?.charAt(0) || "U"}${usuario?.apellido?.charAt(0) || ""}`.toUpperCase();

  // Próxima reserva activa
  const proximaReserva = reservasActivas[0];

  return (
    <div className="fz-client-layout">
      {/* ── SIDEBAR CORPORATIVO DEL CLIENTE ── */}
      <aside className="fz-client-sidebar">
        <div style={{ textAlign: "center", marginBottom: "16px", display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}>
          <img
            src="/logo-futbolzone.png"
            alt="FutbolZone"
            className="fz-brand-logo-emblem"
            style={{ width: "36px", height: "36px" }}
          />
          <strong style={{ fontSize: "14px", color: "#ffffff", letterSpacing: "0.5px" }}>FUTBOLZONE</strong>
        </div>

        <div className="fz-client-user-box">
          <div
            className="fz-client-avatar-halo"
            onClick={() => setTabActiva("perfil")}
            title="Haz clic para actualizar tu información"
          >
            <div className="fz-client-avatar-inner">
              {avatarUrl && avatarUrl.startsWith("data:image") ? (
                <img src={avatarUrl} alt="Avatar" className="fz-avatar-img-custom" />
              ) : (
                <span className="fz-avatar-initials-txt">{iniciales}</span>
              )}
            </div>
          </div>

          <h3 className="fz-client-name">
            {usuario?.nombre || "CLIENTE"} {usuario?.apellido || ""}
          </h3>
          <p className="fz-client-email">{usuario?.email || "cliente@futbolzone.com"}</p>
          <span className="fz-client-role-badge">{rolBadge}</span>
        </div>

        <nav className="fz-client-nav">
          <button
            type="button"
            className={`fz-client-nav-btn ${tabActiva === "resumen" ? "active" : ""}`}
            onClick={() => setTabActiva("resumen")}
          >
            <span>Resumen General</span>
          </button>

          <button
            type="button"
            className={`fz-client-nav-btn ${tabActiva === "reservas" ? "active" : ""}`}
            onClick={() => setTabActiva("reservas")}
          >
            <span>Mis Reservas ({misReservas.length})</span>
          </button>

          <button
            type="button"
            className={`fz-client-nav-btn ${tabActiva === "torneos" ? "active" : ""}`}
            onClick={() => setTabActiva("torneos")}
          >
            <span>Torneos y Ligas</span>
          </button>

          <button
            type="button"
            className={`fz-client-nav-btn ${tabActiva === "retos" ? "active" : ""}`}
            onClick={() => setTabActiva("retos")}
          >
            <span>Tablón de Retos</span>
          </button>

          <button
            type="button"
            className={`fz-client-nav-btn ${tabActiva === "perfil" ? "active" : ""}`}
            onClick={() => setTabActiva("perfil")}
          >
            <span>Mi Perfil y Seguridad</span>
          </button>
        </nav>

        <div className="fz-client-sidebar-footer">
          <button type="button" className="fz-btn-book-cta" onClick={onGoToBooking}>
            + Reservar Cancha
          </button>
          <button type="button" className="fz-client-logout-btn" onClick={onLogout}>
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* ── CONTENIDO PRINCIPAL ── */}
      <main className="fz-client-main">
        {/* Encabezado Superior */}
        <header className="fz-client-top-bar">
          <div>
            <div className="fz-client-breadcrumb">Panel de Usuario › FutbolZone ADSO III</div>
            <h1 className="fz-client-view-title">
              {tabActiva === "resumen" && `Bienvenido, ${usuario?.nombre || "Jugador"}`}
              {tabActiva === "reservas" && "Historial y Gestión de Reservas"}
              {tabActiva === "torneos" && "Torneos y Competencias Oficiales"}
              {tabActiva === "retos" && "Comunidad y Tablón de Retos"}
              {tabActiva === "perfil" && "Configuración de Perfil y Cuenta"}
            </h1>
            {cargando && <div className="fz-sync-status">Sincronizando información...</div>}
          </div>

          <div className="fz-client-top-actions">
            <NotificacionesPill
              key={usuario?.id}
              onNavigate={() => setTabActiva("reservas")}
            />
            <button type="button" className="fz-btn-primary" onClick={onGoToBooking}>
              + Nueva Reserva
            </button>
            <button type="button" className="fz-btn-refresh" onClick={cargarReservas}>
              Actualizar
            </button>
          </div>
        </header>

        {mensaje && (
          <div className="fz-client-banner-alert">
            <span>{mensaje}</span>
          </div>
        )}

        {/* ── TAB 1: RESUMEN GENERAL ── */}
        {tabActiva === "resumen" && (
          <div className="fz-client-tab-content">
            {/* 4 KPIs Ejecutivos */}
            <div className="fz-kpi-grid">
              <div className="fz-kpi-card fz-kpi-highlight">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">TOTAL INVERTIDO</span>
                  <span className="fz-kpi-badge-pill">REGISTRO AL DÍA</span>
                </div>
                <div className="fz-kpi-value">${totalInvertidoReal.toLocaleString("es-CO")} COP</div>
                <div className="fz-kpi-sub">Gasto acumulado en turnos y servicios</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">PARTIDOS JUGADOS</span>
                  <span className="fz-kpi-badge-neutral">{rolBadge}</span>
                </div>
                <div className="fz-kpi-value">{partidosJugadosReal}</div>
                <div className="fz-kpi-sub">Encuentros completados exitosamente</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">RESERVAS ACTIVAS</span>
                  <span className="fz-kpi-badge-success">{reservasActivas.length} VIGENTES</span>
                </div>
                <div className="fz-kpi-value">{reservasActivas.length}</div>
                <div className="fz-kpi-sub">Turnos agendados próximos a disputar</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">PUNTOS DE FIDELIDAD</span>
                  <span className="fz-kpi-badge-neutral">CLUB ZONE</span>
                </div>
                <div className="fz-kpi-value">{partidosJugadosReal * 150} pts</div>
                <div className="fz-kpi-sub">Canjeables por kits y descuentos</div>
              </div>
            </div>

            {/* Desglose Personal de Estados de Reserva */}
            <div className="fz-kpi-grid" style={{ marginTop: "14px" }}>
              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">TOTAL RESERVAS</span>
                  <span className="fz-kpi-badge-neutral">HISTORIAL</span>
                </div>
                <div className="fz-kpi-value">{totalReservasReal}</div>
                <div className="fz-kpi-sub">Solicitudes registradas en tu cuenta</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">PENDIENTES</span>
                  <span className="fz-kpi-badge-neutral">POR APROBAR</span>
                </div>
                <div className="fz-kpi-value">{pendientesReal}</div>
                <div className="fz-kpi-sub">Esperando respuesta del administrador</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">CONFIRMADAS</span>
                  <span className="fz-kpi-badge-success">APROBADAS</span>
                </div>
                <div className="fz-kpi-value">{confirmadasReal}</div>
                <div className="fz-kpi-sub">Turnos aprobados y listos para jugar</div>
              </div>

              <div className="fz-kpi-card">
                <div className="fz-kpi-top">
                  <span className="fz-kpi-label">RECHAZADAS</span>
                  <span className="fz-kpi-badge-neutral">NO APROBADAS</span>
                </div>
                <div className="fz-kpi-value">{rechazadasReal}</div>
                <div className="fz-kpi-sub">Solicitudes rechazadas</div>
              </div>
            </div>

            {/* Próximo Partido Destacado */}
            <div className="fz-client-highlight-banner">
              <div className="fz-highlight-info">
                <span className="fz-highlight-tag">PRÓXIMO PARTIDO AGENDADO</span>
                {proximaReserva ? (
                  <>
                    <h3>{proximaReserva.cancha_nombre || "Cancha Central"}</h3>
                    <p>
                      Fecha: <strong>{proximaReserva.fecha}</strong> | Horario:{" "}
                      <strong>
                        {proximaReserva.hora_inicio?.substring(0, 5)} - {proximaReserva.hora_fin?.substring(0, 5)}
                      </strong>
                    </p>
                  </>
                ) : (
                  <>
                    <h3>No tienes ningún partido agendado próximamente</h3>
                    <p>Elige tu cancha favorita y reserva tu turno en segundos sin esperas ni llamadas.</p>
                  </>
                )}
              </div>
              <button
                type="button"
                className="fz-btn-primary"
                onClick={proximaReserva ? () => setReservaParaTicket(proximaReserva) : onGoToBooking}
              >
                {proximaReserva ? "Ver Comprobante Oficial" : "Reservar Ahora"}
              </button>
            </div>

            {/* Tabla de Reservas Recientes */}
            <div className="fz-subview-card" style={{ marginTop: "24px" }}>
              <div className="fz-table-filters">
                <div className="fz-filters-left">
                  <span className="fz-filter-title">Últimas Reservas Realizadas</span>
                </div>
                <button
                  type="button"
                  className="fz-btn-export-excel"
                  onClick={() => setTabActiva("reservas")}
                >
                  Ver Todas las Reservas ({misReservas.length})
                </button>
              </div>

              <div className="fz-table-responsive">
                <table className="fz-data-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Cancha</th>
                      <th>Fecha & Horario</th>
                      <th>Total</th>
                      <th>Estado</th>
                      <th>Comprobante</th>
                    </tr>
                  </thead>
                  <tbody>
                    {misReservas.length === 0 ? (
                      <tr>
                        <td colSpan={6} style={{ textAlign: "center", padding: "30px", color: "#64748b" }}>
                          Aún no has registrado ninguna reserva.
                        </td>
                      </tr>
                    ) : (
                      misReservas.slice(0, 5).map((r) => (
                        <tr key={r.id}>
                          <td><strong>#{r.id}</strong></td>
                          <td>
                            <div className="fz-cancha-reserved-badge">
                              <span className="fz-reserved-dot" />
                              <strong className="fz-cancha-name-highlight">{r.cancha_nombre || "Cancha Central"}</strong>
                            </div>
                            <div className="fz-cancha-status-sub">
                              <span>✓ Apartada</span>
                            </div>
                          </td>
                          <td>
                            {r.fecha}
                            <div className="fz-time-sub">{r.hora_inicio?.substring(0, 5)} - {r.hora_fin?.substring(0, 5)}</div>
                          </td>
                          <td><strong>${(Number(r.precio_total) || 50000).toLocaleString("es-CO")} COP</strong></td>
                          <td>
                            <span className={`fz-badge-status ${r.estado}`}>
                              {r.estado === "confirmada"  && "✅ CONFIRMADA"}
                              {r.estado === "pendiente"   && "⏳ PENDIENTE DE APROBACIÓN"}
                              {r.estado === "completada"  && "🏆 COMPLETADA"}
                              {r.estado === "cancelada"   && "🚫 CANCELADA"}
                              {r.estado === "rechazada"   && "❌ RECHAZADA"}
                              {!["confirmada","pendiente","completada","cancelada","rechazada"].includes(r.estado) && r.estado?.toUpperCase()}
                            </span>
                          </td>
                          <td>
                            <button
                              type="button"
                              className="fz-btn-action-complete"
                              onClick={() => setReservaParaTicket(r)}
                            >
                              Ver Comprobante
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ── TAB 2: TODAS MIS RESERVAS (BÚSQUEDA Y FILTROS INTEGRADOS) ── */}
        {tabActiva === "reservas" && (
          <div className="fz-subview-card">
            {/* CABECERA Y EXPORTACIÓN */}
            <div className="fz-table-filters">
              <div className="fz-filters-left">
                <span className="fz-filter-title">Historial de Turnos y Reservas</span>
                <span className="fz-results-count-badge">
                  Mostrando {misReservasFiltradas.length} de {misReservas.length} reservas
                </span>
              </div>
              <div className="fz-filters-right-actions">
                {hayFiltrosActivos && (
                  <button
                    type="button"
                    className="fz-btn-clear-filters"
                    onClick={limpiarFiltros}
                    title="Restablecer todos los filtros y ver historial completo"
                  >
                    ✕ Limpiar Filtros
                  </button>
                )}
                <button
                  type="button"
                  className="fz-btn-export-excel"
                  onClick={exportarExcelMisReservas}
                  title="Exportar registros filtrados a archivo Excel (.xlsx)"
                >
                  Descargar (.xlsx)
                </button>
              </div>
            </div>

            {/* ── BARRA DE BÚSQUEDA Y FILTRADO DEPORTIVO ── */}
            <div className="fz-booking-filters-panel">
              {/* 1. Barra de Búsqueda por Texto */}
              <div className="fz-search-box-wrap">
                <span className="fz-search-icon">🔍</span>
                <input
                  type="text"
                  placeholder="Buscar por ID (#), cancha, fecha, estado o método de pago..."
                  value={busquedaTexto}
                  onChange={(e) => setBusquedaTexto(e.target.value)}
                  className="fz-filter-search-input"
                />
                {busquedaTexto && (
                  <button
                    type="button"
                    className="fz-btn-input-clear"
                    onClick={() => setBusquedaTexto("")}
                    title="Borrar búsqueda"
                  >
                    ✕
                  </button>
                )}
              </div>

              {/* 2. Filtro Rápido por Cancha Deportiva */}
              <div className="fz-filter-section-row">
                <span className="fz-filter-label">⚽ Cancha:</span>
                <div className="fz-court-pills-row">
                  <button
                    type="button"
                    className={`fz-court-pill ${filtroCancha === "todas" ? "active" : ""}`}
                    onClick={() => setFiltroCancha("todas")}
                  >
                    Todas ({conteoCanchas.total})
                  </button>
                  <button
                    type="button"
                    className={`fz-court-pill ${filtroCancha === "Cancha Central" ? "active" : ""}`}
                    onClick={() => setFiltroCancha(filtroCancha === "Cancha Central" ? "todas" : "Cancha Central")}
                  >
                    🏟️ Cancha Central ({conteoCanchas.central})
                  </button>
                  <button
                    type="button"
                    className={`fz-court-pill ${filtroCancha === "Cancha Norte" ? "active" : ""}`}
                    onClick={() => setFiltroCancha(filtroCancha === "Cancha Norte" ? "todas" : "Cancha Norte")}
                  >
                    📍 Cancha Norte ({conteoCanchas.norte})
                  </button>
                  <button
                    type="button"
                    className={`fz-court-pill ${filtroCancha === "Cancha Sur" ? "active" : ""}`}
                    onClick={() => setFiltroCancha(filtroCancha === "Cancha Sur" ? "todas" : "Cancha Sur")}
                  >
                    ⚡ Cancha Sur ({conteoCanchas.sur})
                  </button>
                </div>
              </div>

              {/* 3. Filtro por Fecha (Puntual o Rango) */}
              <div className="fz-filter-section-row fz-date-filter-row">
                <span className="fz-filter-label">📅 Fecha:</span>
                <div className="fz-date-mode-pills">
                  <button
                    type="button"
                    className={`fz-date-mode-btn ${filtroFechaModo === "todas" ? "active" : ""}`}
                    onClick={() => {
                      setFiltroFechaModo("todas");
                      setFechaExacta("");
                      setFechaDesde("");
                      setFechaHasta("");
                    }}
                  >
                    Cualquier Fecha
                  </button>
                  <button
                    type="button"
                    className={`fz-date-mode-btn ${filtroFechaModo === "exacta" ? "active" : ""}`}
                    onClick={() => setFiltroFechaModo("exacta")}
                  >
                    Fecha Específica
                  </button>
                  <button
                    type="button"
                    className={`fz-date-mode-btn ${filtroFechaModo === "rango" ? "active" : ""}`}
                    onClick={() => setFiltroFechaModo("rango")}
                  >
                    Rango de Fechas
                  </button>
                </div>

                {/* Input de Fecha Específica */}
                {filtroFechaModo === "exacta" && (
                  <div className="fz-date-picker-inline">
                    <input
                      type="date"
                      value={fechaExacta}
                      onChange={(e) => setFechaExacta(e.target.value)}
                      className="fz-date-input"
                    />
                    {fechaExacta && (
                      <button
                        type="button"
                        className="fz-btn-input-clear-sm"
                        onClick={() => setFechaExacta("")}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                )}

                {/* Inputs de Rango (Desde / Hasta) */}
                {filtroFechaModo === "rango" && (
                  <div className="fz-date-range-inline">
                    <div className="fz-date-range-field">
                      <label>Desde:</label>
                      <input
                        type="date"
                        value={fechaDesde}
                        onChange={(e) => setFechaDesde(e.target.value)}
                        className="fz-date-input"
                      />
                    </div>
                    <div className="fz-date-range-field">
                      <label>Hasta:</label>
                      <input
                        type="date"
                        value={fechaHasta}
                        onChange={(e) => setFechaHasta(e.target.value)}
                        className="fz-date-input"
                      />
                    </div>
                    {(fechaDesde || fechaHasta) && (
                      <button
                        type="button"
                        className="fz-btn-input-clear-sm"
                        onClick={() => {
                          setFechaDesde("");
                          setFechaHasta("");
                        }}
                      >
                        ✕
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* TABLA DE RESULTADOS O ESTADO VACÍO AGRADABLE */}
            <div className="fz-table-responsive">
              <table className="fz-data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Cancha</th>
                    <th>Fecha & Horario</th>
                    <th>Total</th>
                    <th>Método de Pago</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {misReservas.length === 0 ? (
                    <tr>
                      <td colSpan={7} style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
                        <div className="fz-empty-state-box">
                          <span style={{ fontSize: "36px" }}>⚽</span>
                          <h4>Aún no has registrado ninguna reserva</h4>
                          <p>Reserva tu cancha favorita y aparecerá automáticamente en tu historial personal.</p>
                          <button type="button" className="fz-btn-primary" onClick={onGoToBooking} style={{ marginTop: "12px" }}>
                            Reservar Turno Ahora
                          </button>
                        </div>
                      </td>
                    </tr>
                  ) : misReservasFiltradas.length === 0 ? (
                    <tr>
                      <td colSpan={7} style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
                        <div className="fz-empty-state-box">
                          <span style={{ fontSize: "36px" }}>🔍</span>
                          <h4>No se encontraron reservas con esos criterios</h4>
                          <p>No hay partidos registrados que coincidan con la cancha, fechas o texto buscado.</p>
                          <button type="button" className="fz-btn-primary" onClick={limpiarFiltros} style={{ marginTop: "12px" }}>
                            Restablecer Filtros y Ver Todas
                          </button>
                        </div>
                      </td>
                    </tr>
                  ) : (
                    misReservasFiltradas.map((r) => {
                      const metodo = r.metodo_pago || (r.notas?.includes("NEQUI") ? "Nequi" : r.notas?.includes("DAVIPLATA") ? "Daviplata" : r.notas?.includes("TARJETA") ? "Tarjeta" : "Efectivo");
                      return (
                        <tr key={r.id}>
                          <td><strong>#{r.id}</strong></td>
                          <td>
                            <div className="fz-cancha-reserved-badge">
                              <span className="fz-reserved-dot" />
                              <strong className="fz-cancha-name-highlight">{r.cancha_nombre || "Cancha Sintética"}</strong>
                            </div>
                            <div className="fz-cancha-status-sub">
                              <span>✓ Cancha Apartada</span>
                              {r.notas?.includes("Productos:") && !r.notas?.includes("Productos: Ninguno") && (
                                <span className="fz-has-extras-pill" title="Servicios y productos adicionales registrados en el comprobante">
                                  + Servicios Extras
                                </span>
                              )}
                            </div>
                          </td>
                          <td>
                            {r.fecha}
                            <div className="fz-time-sub">{r.hora_inicio?.substring(0, 5)} - {r.hora_fin?.substring(0, 5)}</div>
                          </td>
                          <td><strong>${(Number(r.precio_total) || 50000).toLocaleString("es-CO")} COP</strong></td>
                          <td>{metodo}</td>
                          <td>
                            <span className={`fz-badge-status ${r.estado}`}>
                              {r.estado === "confirmada"  && "✅ CONFIRMADA"}
                              {r.estado === "pendiente"   && "⏳ PENDIENTE DE APROBACIÓN"}
                              {r.estado === "completada"  && "🏆 COMPLETADA"}
                              {r.estado === "cancelada"   && "🚫 CANCELADA"}
                              {r.estado === "rechazada"   && "❌ RECHAZADA"}
                              {!["confirmada","pendiente","completada","cancelada","rechazada"].includes(r.estado) && r.estado?.toUpperCase()}
                            </span>
                          </td>
                          <td>
                            <div className="fz-action-btns">
                              <button
                                type="button"
                                className="fz-btn-action-complete"
                                onClick={() => setReservaParaTicket(r)}
                              >
                                Comprobante
                              </button>
                              {r.estado !== "cancelada" && r.estado !== "completada" && (
                                <button
                                  type="button"
                                  className="fz-btn-action-cancel"
                                  onClick={() => cancelarReserva(r.id)}
                                >
                                  Cancelar
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ── TAB 3: TORNEOS ── */}
        {tabActiva === "torneos" && <TorneosView />}

        {/* ── TAB 4: TABLÓN DE RETOS ── */}
        {tabActiva === "retos" && <TablonRetos usuario={usuario} />}

        {/* ── TAB 5: MI PERFIL Y SEGURIDAD ── */}
        {tabActiva === "perfil" && (
          <div className="fz-subview-card">
            <h3>Información del Titular</h3>
            <p className="fz-form-subtitle">Actualiza tus datos de contacto y credenciales de acceso.</p>

            <form onSubmit={guardarPerfil} className="fz-form-inline">
              <div className="fz-form-grid">
                <div className="fz-field">
                  <label>Nombre *</label>
                  <input
                    type="text"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                    required
                  />
                </div>

                <div className="fz-field">
                  <label>Apellido *</label>
                  <input
                    type="text"
                    value={apellido}
                    onChange={(e) => setApellido(e.target.value)}
                    required
                  />
                </div>

                <div className="fz-field">
                  <label>Correo Electrónico (No modificable)</label>
                  <input
                    type="email"
                    value={usuario?.email || ""}
                    disabled
                    style={{ background: "#e2e8f0", cursor: "not-allowed" }}
                  />
                </div>

                <div className="fz-field">
                  <label>Teléfono / WhatsApp</label>
                  <input
                    type="tel"
                    value={telefono}
                    onChange={(e) => setTelefono(e.target.value)}
                    placeholder="3001234567"
                  />
                </div>
              </div>

              {mensajePerfil && (
                <div className={`fz-alert-${mensajePerfil.tipo === "exito" ? "success" : "error"}`} style={{ marginTop: "16px" }}>
                  {mensajePerfil.texto}
                </div>
              )}

              <div className="fz-form-actions">
                <button type="submit" className="fz-btn-primary" disabled={guardandoPerfil}>
                  {guardandoPerfil ? "Guardando..." : "Actualizar Datos"}
                </button>
                <button
                  type="button"
                  className="fz-btn-outline"
                  onClick={() => setMostrarModalRecuperar(true)}
                >
                  Cambiar Contraseña
                </button>
              </div>
            </form>

            <div style={{ marginTop: "24px" }}>
              <h4>Foto de Perfil</h4>
              <p style={{ fontSize: "12px", color: "#64748b" }}>Sube una foto personalizada para tu carnet de jugador (Máx 2MB).</p>
              <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
                <input
                  type="file"
                  accept="image/*"
                  ref={fileInputRef}
                  style={{ display: "none" }}
                  onChange={handleSubirFoto}
                />
                <button
                  type="button"
                  className="fz-btn-outline"
                  onClick={() => fileInputRef.current?.click()}
                >
                  Seleccionar Imagen
                </button>
                {avatarUrl && (
                  <button type="button" className="fz-btn-danger-sm" onClick={eliminarFoto}>
                    Quitar Foto
                  </button>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Modal de Comprobante Oficial */}
      {reservaParaTicket && (
        <TicketReservaModal
          reserva={reservaParaTicket}
          usuario={usuario}
          onClose={() => setReservaParaTicket(null)}
        />
      )}

      {/* Modal de Cambio de Clave */}
      {mostrarModalRecuperar && (
        <RecuperarPasswordModal
          emailInicial={usuario?.email}
          onClose={() => setMostrarModalRecuperar(false)}
          onSuccessLogin={() => setMostrarModalRecuperar(false)}
        />
      )}
    </div>
  );
}

export default DashboardCliente;
