import React, { useState, useEffect } from "react";
import "./PerfilJugadorModal.css";
import { api, getStoredUser } from "../services/api";

interface PerfilJugadorModalProps {
  jugadorId: number;
  esPropioPerfil?: boolean;
  onClose: () => void;
  onPerfilActualizado?: (usuarioActualizado: any) => void;
}

const AVATARES_PRESET = [
  "https://api.dicebear.com/7.x/bottts/svg?seed=NicoGoleador",
  "https://api.dicebear.com/7.x/bottts/svg?seed=CarlosCrack",
  "https://api.dicebear.com/7.x/bottts/svg?seed=Mateo10",
  "https://api.dicebear.com/7.x/bottts/svg?seed=CapitanSena",
  "https://api.dicebear.com/7.x/bottts/svg?seed=FalcaoFutbol",
  "https://api.dicebear.com/7.x/bottts/svg?seed=JamesZone"
];

export const PerfilJugadorModal: React.FC<PerfilJugadorModalProps> = ({
  jugadorId,
  esPropioPerfil: _esPropioPerfil = false,
  onClose,
  onPerfilActualizado,
}) => {
  const usuarioSesion = getStoredUser();
  const [cargando, setCargando] = useState<boolean>(true);
  const [perfil, setPerfil] = useState<any | null>(null);
  const [modoEdicion, setModoEdicion] = useState<boolean>(false);
  const [mensaje, setMensaje] = useState<{ texto: string; tipo: "exito" | "error" } | null>(null);

  // Formulario de edición propia
  const [formData, setFormData] = useState({
    nombre: "",
    apellido: "",
    username: "",
    posicion: "Delantero",
    dorsal: 10,
    pie_habil: "Derecho",
    bio: "",
    avatar: "",
    telefono: "",
  });

  // Formulario de calificación hacia este jugador
  const [mostrarFormCalificar, setMostrarFormCalificar] = useState<boolean>(false);
  const [ratingEstrellas, setRatingEstrellas] = useState<number>(5);
  const [comentarioRating, setComentarioRating] = useState<string>("");
  const [enviandoRating, setEnviandoRating] = useState<boolean>(false);

  useEffect(() => {
    cargarPerfil();
  }, [jugadorId]);

  const cargarPerfil = async () => {
    setCargando(true);
    try {
      const res = await api.obtenerPerfilDeportivo(jugadorId);
      if (res.success && res.data) {
        setPerfil(res.data);
        setFormData({
          nombre: res.data.nombre || "",
          apellido: res.data.apellido || "",
          username: res.data.username || "",
          posicion: res.data.posicion || "Delantero",
          dorsal: res.data.dorsal || 10,
          pie_habil: res.data.pie_habil || "Derecho",
          bio: res.data.bio || "",
          avatar: res.data.avatar || AVATARES_PRESET[0],
          telefono: res.data.telefono || "",
        });
      }
    } catch (err: any) {
      setMensaje({ texto: "Error al cargar la ficha del jugador", tipo: "error" });
    } finally {
      setCargando(false);
    }
  };

  const guardarCambios = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.actualizarPerfilDeportivo(jugadorId, formData);
      if (res.success) {
        setPerfil(res.data);
        setModoEdicion(false);
        setMensaje({ texto: "¡Ficha deportiva actualizada exitosamente!", tipo: "exito" });
        if (onPerfilActualizado) {
          onPerfilActualizado(res.data);
        }
      } else {
        setMensaje({ texto: res.message || "Error al actualizar perfil", tipo: "error" });
      }
    } catch (err: any) {
      setMensaje({ texto: err.message || "Error al conectar con el servidor", tipo: "error" });
    }
  };

  const enviarCalificacion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!usuarioSesion) {
      alert("Debes iniciar sesión para calificar a un compañero.");
      return;
    }
    setEnviandoRating(true);
    try {
      const res = await api.calificarJugador({
        jugador_id: jugadorId,
        estrellas: ratingEstrellas,
        comentario: comentarioRating,
      });
      if (res.success) {
        setMensaje({ texto: "¡Valoración registrada con éxito!", tipo: "exito" });
        setMostrarFormCalificar(false);
        setComentarioRating("");
        cargarPerfil();
      } else {
        setMensaje({ texto: res.message || "No se pudo registrar la calificación", tipo: "error" });
      }
    } catch (err: any) {
      setMensaje({ texto: err.message || "Error al registrar la valoración", tipo: "error" });
    } finally {
      setEnviandoRating(false);
    }
  };

  const esMismoUsuario = usuarioSesion && Number(usuarioSesion.id) === Number(jugadorId);

  return (
    <div className="fz-modal-backdrop-profile" onClick={onClose}>
      <div className="fz-modal-content-profile" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="btn-close-modal-p" onClick={onClose}>
          ✕
        </button>

        {cargando ? (
          <div className="fz-profile-loading">
            <span className="spinner-ball">⚽</span>
            <p>Cargando ficha del futbolista...</p>
          </div>
        ) : perfil ? (
          <div className="fz-profile-card-container">
            {/* CABECERA: TARJETA DEPORTIVA TIPO CARTA FUTBOLÍSTICA */}
            <div className="fz-fut-card">
              <div className="fut-card-header">
                <div className="fut-card-ovr">
                  <span className="ovr-num">{Math.round(perfil.estadisticas?.calificacion_promedio * 19.5) || 94}</span>
                  <span className="ovr-pos">{perfil.posicion?.substring(0, 3).toUpperCase()}</span>
                </div>
                <div className="fut-card-dorsal">#{perfil.dorsal}</div>
              </div>

              <div className="fut-card-avatar-wrap">
                <img src={perfil.avatar || AVATARES_PRESET[0]} alt={perfil.nombre_completo} className="fut-avatar" />
              </div>

              <div className="fut-card-name-band">
                <h3>{perfil.nombre}</h3>
                <span className="fut-username">{perfil.username}</span>
              </div>

              {/* RATING ESTRELLAS Y MEDALLA */}
              <div className="fut-card-rating-bar">
                <div className="stars-gold">
                  {"★".repeat(Math.round(perfil.estadisticas?.calificacion_promedio || 5))}
                  {"☆".repeat(5 - Math.round(perfil.estadisticas?.calificacion_promedio || 5))}
                </div>
                <span className="rating-num">
                  {perfil.estadisticas?.calificacion_promedio || 5.0} ({perfil.estadisticas?.total_valoraciones || 0} votos)
                </span>
              </div>

              {/* ATRIBUTOS DEPORTIVOS */}
              <div className="fut-attributes-grid">
                <div className="att-item">
                  <span className="att-label">POSICIÓN</span>
                  <strong className="att-val">{perfil.posicion}</strong>
                </div>
                <div className="att-item">
                  <span className="att-label">PIE HÁBIL</span>
                  <strong className="att-val">{perfil.pie_habil}</strong>
                </div>
                <div className="att-item">
                  <span className="att-label">PARTIDOS</span>
                  <strong className="att-val">{perfil.estadisticas?.partidos_totales || 0}</strong>
                </div>
                <div className="att-item">
                  <span className="att-label">COMPLETADOS</span>
                  <strong className="att-val">{perfil.estadisticas?.partidos_completados || 0}</strong>
                </div>
              </div>
            </div>

            {/* SECCIÓN DETALLADA Y EDICIÓN */}
            <div className="fz-profile-details-pane">
              <div className="pane-header-row">
                <div>
                  <h2>Ficha Oficial del Jugador</h2>
                  <span className="member-since">Miembro desde {perfil.fecha_registro?.substring(0, 10)}</span>
                </div>
                {esMismoUsuario && (
                  <button
                    type="button"
                    className="btn-toggle-edit"
                    onClick={() => setModoEdicion(!modoEdicion)}
                  >
                    {modoEdicion ? "Cancelar Edición" : "✏️ Editar Mi Ficha"}
                  </button>
                )}
              </div>

              {mensaje && (
                <div className={`fz-profile-alert ${mensaje.tipo}`}>
                  {mensaje.tipo === "exito" ? "✅" : "⚠️"} {mensaje.texto}
                </div>
              )}

              {/* VISTA DE EDICIÓN */}
              {modoEdicion ? (
                <form onSubmit={guardarCambios} className="fz-edit-profile-form">
                  <div className="form-group-avatar-pick">
                    <label>Elige tu Avatar de Futbolista:</label>
                    <div className="avatar-pick-grid">
                      {AVATARES_PRESET.map((av, idx) => (
                        <img
                          key={idx}
                          src={av}
                          alt={`Avatar ${idx + 1}`}
                          className={`avatar-choice ${formData.avatar === av ? "selected" : ""}`}
                          onClick={() => setFormData({ ...formData, avatar: av })}
                        />
                      ))}
                    </div>
                  </div>

                  <div className="form-row-2">
                    <div className="f-field">
                      <label>Nombre:</label>
                      <input
                        type="text"
                        value={formData.nombre}
                        onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                        required
                      />
                    </div>
                    <div className="f-field">
                      <label>Apellido:</label>
                      <input
                        type="text"
                        value={formData.apellido}
                        onChange={(e) => setFormData({ ...formData, apellido: e.target.value })}
                        required
                      />
                    </div>
                  </div>

                  <div className="form-row-3">
                    <div className="f-field">
                      <label>Username (@):</label>
                      <input
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                        required
                      />
                    </div>
                    <div className="f-field">
                      <label>Posición:</label>
                      <select
                        value={formData.posicion}
                        onChange={(e) => setFormData({ ...formData, posicion: e.target.value })}
                      >
                        <option value="Delantero">Delantero</option>
                        <option value="Mediocampista">Mediocampista</option>
                        <option value="Extremo">Extremo</option>
                        <option value="Defensa Central">Defensa Central</option>
                        <option value="Lateral">Lateral</option>
                        <option value="Portero / Arquero">Portero / Arquero</option>
                      </select>
                    </div>
                    <div className="f-field">
                      <label>Dorsal (#):</label>
                      <input
                        type="number"
                        min="1"
                        max="99"
                        value={formData.dorsal}
                        onChange={(e) => setFormData({ ...formData, dorsal: Number(e.target.value) })}
                      />
                    </div>
                  </div>

                  <div className="form-row-2">
                    <div className="f-field">
                      <label>Pie Hábil:</label>
                      <select
                        value={formData.pie_habil}
                        onChange={(e) => setFormData({ ...formData, pie_habil: e.target.value })}
                      >
                        <option value="Derecho">Derecho</option>
                        <option value="Izquierdo">Izquierdo (Zurdo)</option>
                        <option value="Ambidiestro">Ambidiestro</option>
                      </select>
                    </div>
                    <div className="f-field">
                      <label>Teléfono:</label>
                      <input
                        type="text"
                        value={formData.telefono}
                        onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                      />
                    </div>
                  </div>

                  <div className="f-field">
                    <label>Presentación / Biografía Futbolera:</label>
                    <textarea
                      rows={3}
                      value={formData.bio}
                      onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                      placeholder="Describe tu estilo de juego, tus fortalezas tácticas y tu disponibilidad..."
                    />
                  </div>

                  <div className="form-actions-bar">
                    <button type="submit" className="btn-save-profile">
                      💾 Guardar Ficha Deportiva
                    </button>
                    <button type="button" className="btn-cancel-edit" onClick={() => setModoEdicion(false)}>
                      Cancelar
                    </button>
                  </div>
                </form>
              ) : (
                /* VISTA DE INFORMACIÓN Y COMENTARIOS */
                <div className="fz-profile-bio-box">
                  <div className="bio-paragraph">
                    <h4>Biografía y Estilo de Juego</h4>
                    <p>{perfil.bio || "Este jugador aún no ha agregado una biografía."}</p>
                  </div>

                  <div className="contact-pills">
                    <span className="cpill">📧 {perfil.email}</span>
                    {perfil.telefono && <span className="cpill">📱 {perfil.telefono}</span>}
                    <span className="cpill">⚽ Rol: {perfil.rol?.toUpperCase()}</span>
                  </div>

                  {/* BOTÓN CALIFICAR COMPAÑERO (Si no es el mismo usuario) */}
                  {!esMismoUsuario && usuarioSesion && (
                    <div className="peer-rating-action-card">
                      <div className="peer-action-text">
                        <strong>¿Has jugado un partido con {perfil.nombre}?</strong>
                        <span>Califica su nivel deportivo, juego limpio y compañerismo.</span>
                      </div>
                      <button
                        type="button"
                        className="btn-open-rate-peer"
                        onClick={() => setMostrarFormCalificar(!mostrarFormCalificar)}
                      >
                        {mostrarFormCalificar ? "Cerrar" : "⭐ Calificar a este Jugador"}
                      </button>
                    </div>
                  )}

                  {/* FORMULARIO DESPLEGABLE DE CALIFICACIÓN */}
                  {mostrarFormCalificar && (
                    <form onSubmit={enviarCalificacion} className="peer-rating-form">
                      <h4>Valorar a {perfil.nombre_completo}</h4>
                      <div className="star-picker-row">
                        <span>Puntuación:</span>
                        <div className="interactive-stars">
                          {[1, 2, 3, 4, 5].map((s) => (
                            <button
                              key={s}
                              type="button"
                              className={`btn-star ${ratingEstrellas >= s ? "filled" : ""}`}
                              onClick={() => setRatingEstrellas(s)}
                            >
                              ★
                            </button>
                          ))}
                        </div>
                        <span className="stars-caption">{ratingEstrellas} / 5 Estrellas</span>
                      </div>

                      <textarea
                        rows={2}
                        value={comentarioRating}
                        onChange={(e) => setComentarioRating(e.target.value)}
                        placeholder="Escribe un comentario sobre su rendimiento o juego limpio..."
                        required
                      />

                      <button type="submit" className="btn-submit-rating" disabled={enviandoRating}>
                        {enviandoRating ? "Registrando..." : "Enviar Calificación Oficial"}
                      </button>
                    </form>
                  )}

                  {/* HISTORIAL DE VALORACIONES DE COMPAÑEROS */}
                  <div className="opinions-section">
                    <h4>Opiniones y Reseñas de Compañeros ({perfil.opiniones_recibidas?.length || 0})</h4>
                    {perfil.opiniones_recibidas?.length === 0 ? (
                      <p className="no-opinions">Este jugador aún no tiene valoraciones de otros compañeros.</p>
                    ) : (
                      <div className="opinions-list">
                        {perfil.opiniones_recibidas.map((op: any) => (
                          <div key={op.id} className="opinion-item-card">
                            <div className="op-header">
                              <span className="op-author">⚽ {op.evaluador_nombre}</span>
                              <span className="op-stars">{"★".repeat(op.estrellas)}</span>
                            </div>
                            <p className="op-comment">"{op.comentario || "Gran jugador y excelente compañero."}"</p>
                            <span className="op-date">{op.fecha?.substring(0, 10)}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <p>No se pudo cargar la información del jugador.</p>
        )}
      </div>
    </div>
  );
};

export default PerfilJugadorModal;
