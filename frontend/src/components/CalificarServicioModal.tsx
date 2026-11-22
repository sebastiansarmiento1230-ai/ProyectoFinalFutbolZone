import React, { useState } from "react";
import "./CalificarServicioModal.css";
import { api } from "../services/api";

interface CalificarServicioModalProps {
  reserva: any;
  onClose: () => void;
  onCalificacionEnviada: () => void;
}

export const CalificarServicioModal: React.FC<CalificarServicioModalProps> = ({
  reserva,
  onClose,
  onCalificacionEnviada,
}) => {
  const [atencion, setAtencion] = useState<number>(5);
  const [servicio, setServicio] = useState<number>(5);
  const [instalaciones, setInstalaciones] = useState<number>(5);
  const [experiencia, setExperiencia] = useState<number>(5);
  const [comentario, setComentario] = useState<string>("");
  const [enviando, setEnviando] = useState<boolean>(false);
  const [mensaje, setMensaje] = useState<{ texto: string; tipo: "exito" | "error" } | null>(null);

  const promedioCalculado = ((atencion + servicio + instalaciones + experiencia) / 4.0).toFixed(1);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setEnviando(true);
    setMensaje(null);

    try {
      const res = await api.calificarServicio({
        reserva_id: reserva.id,
        atencion,
        servicio,
        instalaciones,
        experiencia,
        comentario,
      });

      if (res.success) {
        setMensaje({ texto: "¡Gracias por valorar nuestro complejo deportivo!", tipo: "exito" });
        setTimeout(() => {
          onCalificacionEnviada();
          onClose();
        }, 1200);
      } else {
        setMensaje({ texto: res.message || "Error al registrar la valoración", tipo: "error" });
      }
    } catch (err: any) {
      setMensaje({ texto: err.message || "No se pudo conectar con el servidor", tipo: "error" });
    } finally {
      setEnviando(false);
    }
  };

  const renderStars = (valorActual: number, setter: (val: number) => void) => {
    return (
      <div className="fz-star-control">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            className={`btn-star-metric ${valorActual >= star ? "active" : ""}`}
            onClick={() => setter(star)}
          >
            ★
          </button>
        ))}
        <span className="star-metric-val">{valorActual}/5</span>
      </div>
    );
  };

  return (
    <div className="fz-modal-backdrop-service-rate" onClick={onClose}>
      <div className="fz-modal-content-service-rate" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="btn-close-service-rate" onClick={onClose}>
          ✕
        </button>

        <div className="rate-header-badge">
          <span className="badge-ball">⚽</span>
          <h3>Califica tu Experiencia en la Cancha</h3>
          <p>
            Reserva #{reserva.id} · {reserva.cancha_nombre || "Cancha Deportiva"} ({reserva.fecha})
          </p>
        </div>

        {mensaje && (
          <div className={`fz-rate-alert ${mensaje.tipo}`}>
            {mensaje.tipo === "exito" ? "✅" : "⚠️"} {mensaje.texto}
          </div>
        )}

        <form onSubmit={handleSubmit} className="fz-service-rating-form">
          {/* 4 DIMENSIONES OBLIGATORIAS */}
          <div className="dimension-row-card">
            <div className="dim-info">
              <strong>1. Atención al Cliente</strong>
              <span>Amabilidad, puntualidad y disposición del personal de la sede.</span>
            </div>
            {renderStars(atencion, setAtencion)}
          </div>

          <div className="dimension-row-card">
            <div className="dim-info">
              <strong>2. Servicio & Plataforma</strong>
              <span>Facilidad de agendamiento, confirmación y gestión de la reserva.</span>
            </div>
            {renderStars(servicio, setServicio)}
          </div>

          <div className="dimension-row-card">
            <div className="dim-info">
              <strong>3. Instalaciones & Cancha</strong>
              <span>Calidad del césped sintético, iluminación LED, mallas y vestuarios.</span>
            </div>
            {renderStars(instalaciones, setInstalaciones)}
          </div>

          <div className="dimension-row-card">
            <div className="dim-info">
              <strong>4. Experiencia Global</strong>
              <span>Satisfacción general de tu partido y ambiente deportivo vivido.</span>
            </div>
            {renderStars(experiencia, setExperiencia)}
          </div>

          {/* PROMEDIO EN VIVO */}
          <div className="live-average-bar">
            <span>Puntuación Promedio de tu Experiencia:</span>
            <div className="average-pill">
              ⭐ <strong>{promedioCalculado} / 5.0</strong>
            </div>
          </div>

          {/* COMENTARIO */}
          <div className="form-comment-field">
            <label>Comentario y Sugerencias de Mejora (Opcional):</label>
            <textarea
              rows={3}
              value={comentario}
              onChange={(e) => setComentario(e.target.value)}
              placeholder="¿Qué te gustó más? ¿Qué aspectos podemos mejorar para tu próximo partido?"
            />
          </div>

          <button type="submit" className="btn-confirm-service-rate" disabled={enviando}>
            {enviando ? "Guardando Valoración..." : "🏆 Publicar Valoración Oficial"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CalificarServicioModal;
