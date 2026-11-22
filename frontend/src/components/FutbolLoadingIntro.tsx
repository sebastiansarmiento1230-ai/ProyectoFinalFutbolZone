import React, { useState, useEffect } from "react";
import "./FutbolLoadingIntro.css";

interface FutbolLoadingIntroProps {
  onComplete: () => void;
  rolUsuario?: string;
  nombreUsuario?: string;
}

export const FutbolLoadingIntro: React.FC<FutbolLoadingIntroProps> = ({
  onComplete,
  rolUsuario = "cliente",
  nombreUsuario = "Crack",
}) => {
  // Escenas: 1 (Aparición), 2 (Carrera), 3 (Disparo), 4 (Atajada fallida y Gol), 5 (Celebración), 6 (Transición)
  const [escena, setEscena] = useState<1 | 2 | 3 | 4 | 5 | 6>(1);
  const [progreso, setProgreso] = useState<number>(10);
  const [mensajeEscena, setMensajeEscena] = useState<string>("¡Salto al terreno de juego!");

  useEffect(() => {
    // Cronograma cinematográfico de las 6 escenas
    const t1 = setTimeout(() => {
      setEscena(2);
      setProgreso(30);
      setMensajeEscena("Carrera y conducción hacia el arco rival...");
    }, 1400);

    const t2 = setTimeout(() => {
      setEscena(3);
      setProgreso(55);
      setMensajeEscena("¡Cambio de cámara! Perfilando el disparo...");
    }, 3200);

    const t3 = setTimeout(() => {
      setEscena(4);
      setProgreso(75);
      setMensajeEscena("¡El portero vuela pero el balón entra en la escuadra!");
    }, 4700);

    const t4 = setTimeout(() => {
      setEscena(5);
      setProgreso(95);
      setMensajeEscena(`¡GOOOOOOL! ¡Celebración y bienvenida a FutbolZone, ${nombreUsuario}!`);
    }, 6200);

    const t5 = setTimeout(() => {
      setEscena(6);
      setProgreso(100);
      setMensajeEscena("Ingresando al sistema deportivo...");
    }, 7800);

    const tFinal = setTimeout(() => {
      onComplete();
    }, 8500);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      clearTimeout(t4);
      clearTimeout(t5);
      clearTimeout(tFinal);
    };
  }, [onComplete, nombreUsuario]);

  return (
    <div className={`fz-cinematic-stage escena-${escena} ${escena === 6 ? "fade-out" : ""}`}>
      {/* ── ILUMINACIÓN NOCTURNA DEL ESTADIO ── */}
      <div className="fz-stadium-sky">
        <div className="fz-reflector-beam beam-left" />
        <div className="fz-reflector-beam beam-center-left" />
        <div className="fz-reflector-beam beam-center-right" />
        <div className="fz-reflector-beam beam-right" />
        <div className="fz-stadium-lights-glow" />
      </div>

      {/* MARCADOR SUPERIOR CINEMÁTICO */}
      <div className="fz-cinematic-top-header">
        <div className="fz-cinematic-brand-pill">
          <span className="fz-brand-ball">⚽</span>
          <strong>FUTBOL<span>ZONE</span></strong>
          <span className="fz-badge-role">
            {rolUsuario === "admin" ? "👑 MODO ADMINISTRADOR" : "👤 SESIÓN JUGADOR"}
          </span>
        </div>
        <div className="fz-scene-step-indicator">
          <span>ESCENA {escena} DE 6</span>
        </div>
      </div>

      {/* ── ESCENARIO CENTRAL CINEMATOGRÁFICO INTERACTIVO ── */}
      <div className="fz-cinematic-viewport">
        {/* LÍNEAS DE VELOCIDAD ESTILO ANIME (Escena 2 y 3) */}
        {(escena === 2 || escena === 3) && (
          <div className="fz-anime-speed-lines">
            <div className="line l1" />
            <div className="line l2" />
            <div className="line l3" />
            <div className="line l4" />
            <div className="line l5" />
          </div>
        )}

        {/* ══════════════════════════════════════════════════
            VISTA LATERAL DINÁMICA (ESCENA 1 Y ESCENA 2)
            ══════════════════════════════════════════════════ */}
        {(escena === 1 || escena === 2) && (
          <div className={`fz-stage-sideview ${escena === 2 ? "running-mode" : "entry-mode"}`}>
            {/* Césped con franjas y perspectiva */}
            <div className="fz-side-pitch">
              <div className="fz-pitch-stripes-parallax" />
              <div className="fz-center-circle-line" />
              <div className="fz-side-white-line" />
            </div>

            {/* Portería a la derecha */}
            <div className="fz-side-goal-post">
              <div className="side-net-mesh" />
              <div className="side-post-bar" />
            </div>

            {/* PERSONAJE ANIME DEPORTIVO 2.5D (Lateral) */}
            <div className={`fz-anime-player-side ${escena === 2 ? "sprinting" : "ready"}`}>
              {/* Sombra proyectada */}
              <div className="player-shadow-ground" />

              <svg viewBox="0 0 120 140" className="fz-anime-svg">
                <defs>
                  <linearGradient id="jerseyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#10b981" />
                    <stop offset="100%" stopColor="#047857" />
                  </linearGradient>
                  <linearGradient id="hairGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#1e293b" />
                    <stop offset="100%" stopColor="#0f172a" />
                  </linearGradient>
                </defs>

                {/* Pierna izquierda (detrás) */}
                <g className="leg-back">
                  <path d="M50 78 L42 105 L30 126" stroke="#062215" strokeWidth="10" strokeLinecap="round" fill="none" />
                  <path d="M40 102 L32 124" stroke="#10b981" strokeWidth="7" strokeLinecap="round" />
                  {/* Bota de fútbol */}
                  <polygon points="26,128 36,122 34,132 20,132" fill="#0f172a" />
                  <rect x="22" y="132" width="12" height="3" fill="#34d399" rx="1" />
                </g>

                {/* Pierna derecha (conducción activa) */}
                <g className="leg-front">
                  <path d="M68 78 L80 102 L92 124" stroke="#062215" strokeWidth="10" strokeLinecap="round" fill="none" />
                  <path d="M78 98 L88 120" stroke="#10b981" strokeWidth="7" strokeLinecap="round" />
                  {/* Bota de fútbol */}
                  <polygon points="90,126 102,122 104,132 86,132" fill="#0f172a" />
                  <rect x="88" y="132" width="14" height="3" fill="#34d399" rx="1" />
                </g>

                {/* Torso atlético con inclinación */}
                <path d="M44 48 L76 48 L72 82 L46 82 Z" fill="url(#jerseyGrad)" />
                <path d="M48 48 L50 82" stroke="#064e3b" strokeWidth="2" />
                <path d="M70 48 L68 82" stroke="#064e3b" strokeWidth="2" />

                {/* Dorsal 10 brillante */}
                <text x="60" y="70" fontSize="15" fontWeight="900" fill="#ffffff" textAnchor="middle" fontFamily="sans-serif">
                  10
                </text>

                {/* Brazos dinámicos de sprint */}
                <g className="arm-back">
                  <path d="M44 52 L26 68 L16 60" stroke="#fca5a5" strokeWidth="7" strokeLinecap="round" fill="none" />
                </g>
                <g className="arm-front">
                  <path d="M74 52 L92 68 L104 62" stroke="#fca5a5" strokeWidth="7" strokeLinecap="round" fill="none" />
                </g>

                {/* Cuello y Cabeza */}
                <circle cx="60" cy="30" r="14" fill="#fca5a5" />

                {/* Ojos expresivos estilo anime */}
                <ellipse cx="66" cy="30" rx="3" ry="4" fill="#0f172a" />
                <circle cx="67" cy="29" r="1" fill="#ffffff" />

                {/* Cabello anime con picos y dinamismo */}
                <path
                  d="M44 26 C46 12, 60 8, 76 16 C80 20, 78 28, 76 32 C74 24, 68 20, 60 22 C52 24, 48 30, 44 26 Z"
                  fill="url(#hairGrad)"
                />
                <polygon points="46,18 40,8 54,14" fill="url(#hairGrad)" />
                <polygon points="56,12 62,3 68,12" fill="url(#hairGrad)" />
                <polygon points="70,14 80,8 76,22" fill="url(#hairGrad)" />

                {/* Cinta deportiva verde en la frente */}
                <rect x="48" y="24" width="26" height="4" fill="#10b981" rx="1" />
              </svg>
            </div>

            {/* BALÓN DE FÚTBOL CON CONDUCCIÓN */}
            <div className={`fz-anime-ball-side ${escena === 2 ? "dribbling" : "standing"}`}>
              <div className="fz-ball-spin-wrapper">
                <svg viewBox="0 0 36 36" className="fz-ball-svg">
                  <circle cx="18" cy="18" r="16" fill="#ffffff" stroke="#0f172a" strokeWidth="2.5" />
                  <polygon points="18,11 23,15 21,21 15,21 13,15" fill="#0f172a" />
                  <line x1="18" y1="11" x2="18" y2="3" stroke="#0f172a" strokeWidth="2" />
                  <line x1="23" y1="15" x2="31" y2="12" stroke="#0f172a" strokeWidth="2" />
                  <line x1="21" y1="21" x2="28" y2="28" stroke="#0f172a" strokeWidth="2" />
                  <line x1="15" y1="21" x2="8" y2="28" stroke="#0f172a" strokeWidth="2" />
                  <line x1="13" y1="15" x2="5" y2="12" stroke="#0f172a" strokeWidth="2" />
                </svg>
              </div>
            </div>
          </div>
        )}

        {/* ══════════════════════════════════════════════════
            ESCENA 3: DISPARO EN PERSPECTIVA TRASERA (3D BEHIND)
            ══════════════════════════════════════════════════ */}
        {escena === 3 && (
          <div className="fz-stage-shoot-view">
            {/* Cancha en perspectiva hacia la portería */}
            <div className="fz-perspective-pitch">
              <div className="fz-pitch-area-lines" />
              <div className="fz-goal-mouth">
                <div className="fz-post-crossbar" />
                <div className="fz-post-left" />
                <div className="fz-post-right" />
                <div className="fz-post-net-3d" />
              </div>
            </div>

            {/* JUGADOR DE ESPALDAS CARGANDO EL DISPARO */}
            <div className="fz-player-behind-actor">
              <svg viewBox="0 0 100 120" className="fz-behind-svg">
                {/* Sombra */}
                <ellipse cx="50" cy="112" rx="30" ry="8" fill="rgba(0,0,0,0.4)" />
                {/* Pierna de apoyo izquierda */}
                <path d="M42 70 L38 95 L34 114" stroke="#062215" strokeWidth="12" strokeLinecap="round" fill="none" />
                {/* Pierna derecha cargando el chutazo potente */}
                <path d="M58 70 L72 90 L88 104" stroke="#062215" strokeWidth="12" strokeLinecap="round" fill="none" className="shoot-leg-back" />
                {/* Espalda con Dorsal 10 */}
                <path d="M34 38 L66 38 L62 74 L38 74 Z" fill="#10b981" />
                <text x="50" y="60" fontSize="18" fontWeight="900" fill="#ffffff" textAnchor="middle" fontFamily="sans-serif">
                  10
                </text>
                <text x="50" y="46" fontSize="7" fontWeight="800" fill="#ffffff" textAnchor="middle" letterSpacing="1">
                  CRACK
                </text>
                {/* Cabeza de espaldas con pelo puntiagudo */}
                <circle cx="50" cy="24" r="14" fill="#0f172a" />
                <polygon points="40,20 34,10 46,16" fill="#0f172a" />
                <polygon points="48,16 50,6 56,16" fill="#0f172a" />
                <polygon points="56,18 64,10 60,22" fill="#0f172a" />
                <rect x="40" y="24" width="20" height="3" fill="#10b981" />
              </svg>

              {/* Ráfaga de energía del disparo */}
              <div className="fz-shoot-burst" />
            </div>

            {/* BALÓN SALIENDO DISPARADO HACIA EL ARCO EN PERSPECTIVA */}
            <div className="fz-ball-flight-actor">
              <div className="fz-ball-trail-fire" />
              <div className="fz-ball-mini-rot">⚽</div>
            </div>
          </div>
        )}

        {/* ══════════════════════════════════════════════════
            ESCENA 4: ATAJADA FALLIDA DEL PORTERO Y GOL
            ══════════════════════════════════════════════════ */}
        {escena === 4 && (
          <div className="fz-stage-keeper-view">
            {/* Gran Portería Frontal */}
            <div className="fz-front-goal-net goal-hit-shake">
              <div className="fz-front-crossbar" />
              <div className="fz-front-left-post" />
              <div className="fz-front-right-post" />
              <div className="fz-front-mesh-grid" />

              {/* PORTERO RIVAL VOLANDO / ATAJADA FALLIDA */}
              <div className="fz-keeper-actor keeper-dive-miss">
                <svg viewBox="0 0 110 110" className="fz-keeper-svg">
                  {/* Cuerpo del portero en salto diagonal */}
                  <g transform="rotate(35, 55, 55)">
                    {/* Piernas estiradas */}
                    <path d="M40 70 L25 95" stroke="#1e293b" strokeWidth="8" strokeLinecap="round" />
                    <path d="M55 70 L45 98" stroke="#1e293b" strokeWidth="8" strokeLinecap="round" />
                    {/* Buzo de arquero amarillo flúor */}
                    <rect x="36" y="38" width="28" height="34" fill="#facc15" rx="4" />
                    <text x="50" y="58" fontSize="12" fontWeight="900" fill="#000000" textAnchor="middle">1</text>
                    {/* Brazos con guantes estirándose hacia el ángulo */}
                    <path d="M38 42 L20 25 L10 16" stroke="#facc15" strokeWidth="7" strokeLinecap="round" />
                    <path d="M62 42 L78 22 L88 12" stroke="#facc15" strokeWidth="7" strokeLinecap="round" />
                    {/* Guantes de portero */}
                    <circle cx="8" cy="14" r="6" fill="#ef4444" />
                    <circle cx="90" cy="10" r="6" fill="#ef4444" />
                    {/* Cabeza del portero */}
                    <circle cx="50" cy="26" r="10" fill="#f87171" />
                    <path d="M42 20 Q50 12 58 20 Z" fill="#0f172a" />
                  </g>
                </svg>
              </div>

              {/* BALÓN PENETRANDO EN LA ESCUADRA */}
              <div className="fz-ball-in-top-corner">
                <span className="ball-blast">⚽</span>
                <div className="net-impact-wave" />
              </div>
            </div>

            {/* LETRERO DE GOL EXPANSIVO */}
            <div className="fz-super-goal-banner">
              <span className="goal-word">¡GOOOOOOOLAZO!</span>
              <span className="goal-sub">¡DIRECTO A LA ESCUADRA!</span>
            </div>
          </div>
        )}

        {/* ══════════════════════════════════════════════════
            ESCENA 5 Y 6: CELEBRACIÓN Y TRANSICIÓN
            ══════════════════════════════════════════════════ */}
        {(escena === 5 || escena === 6) && (
          <div className="fz-stage-celebration-view">
            {/* Lluvia de confeti y partículas deportivas */}
            <div className="fz-confetti-field">
              {Array.from({ length: 18 }).map((_, i) => (
                <div key={i} className={`confetti-spark s${i + 1}`} />
              ))}
            </div>

            {/* JUGADOR EN PRIMER PLANO CELEBRANDO CON BRAZOS EN ALTO */}
            <div className="fz-celebrating-player">
              <svg viewBox="0 0 120 140" className="fz-celebrate-svg">
                {/* Sombra */}
                <ellipse cx="60" cy="128" rx="36" ry="10" fill="rgba(0,0,0,0.5)" />

                {/* Piernas firmes */}
                <path d="M46 85 L42 124" stroke="#062215" strokeWidth="11" strokeLinecap="round" />
                <path d="M74 85 L78 124" stroke="#062215" strokeWidth="11" strokeLinecap="round" />
                <path d="M42 108 L42 122" stroke="#10b981" strokeWidth="8" strokeLinecap="round" />
                <path d="M78 108 L78 122" stroke="#10b981" strokeWidth="8" strokeLinecap="round" />

                {/* Camiseta 10 */}
                <path d="M38 52 L82 52 L76 88 L44 88 Z" fill="#10b981" />
                <text x="60" y="74" fontSize="16" fontWeight="900" fill="#ffffff" textAnchor="middle">10</text>

                {/* Brazos en alto celebrando con puños */}
                <g className="arms-up">
                  <path d="M40 54 L24 30 L22 14" stroke="#fca5a5" strokeWidth="8" strokeLinecap="round" fill="none" />
                  <circle cx="22" cy="12" r="5" fill="#fca5a5" />
                  <path d="M80 54 L96 30 L98 14" stroke="#fca5a5" strokeWidth="8" strokeLinecap="round" fill="none" />
                  <circle cx="98" cy="12" r="5" fill="#fca5a5" />
                </g>

                {/* Cabeza sonriente con ojos de felicidad */}
                <circle cx="60" cy="34" r="14" fill="#fca5a5" />
                {/* Sonrisa anime */}
                <path d="M54 38 Q60 44 66 38" stroke="#991b1b" strokeWidth="2.5" fill="none" strokeLinecap="round" />
                {/* Ojos cerrados de euforia (^^) */}
                <path d="M52 30 Q55 26 58 30" stroke="#0f172a" strokeWidth="2" fill="none" />
                <path d="M62 30 Q65 26 68 30" stroke="#0f172a" strokeWidth="2" fill="none" />

                {/* Pelo y cinta */}
                <path d="M44 26 C48 10, 72 10, 76 26 Z" fill="#0f172a" />
                <polygon points="46,14 42,4 52,10" fill="#0f172a" />
                <polygon points="56,8 60,1 64,8" fill="#0f172a" />
                <polygon points="68,10 78,4 74,14" fill="#0f172a" />
                <rect x="46" y="24" width="28" height="4" fill="#10b981" rx="1" />
              </svg>
            </div>

            {/* BANNER DE BIENVENIDA OFICIAL */}
            <div className="fz-celebrate-card">
              <span className="celebrate-badge">AUTENTICACIÓN EXITOSA</span>
              <h2>¡GOLAZO! BIENVENIDO A FUTBOLZONE</h2>
              <p>Hola, <strong>{nombreUsuario}</strong>. Entrando a tus reservas deportivas...</p>
            </div>
          </div>
        )}
      </div>

      {/* ── BARRA INFERIOR DE ESTADO TÁCTICO & CONTROL ── */}
      <div className="fz-cinematic-footer">
        <div className="fz-tactical-row">
          <span className="fz-tactical-text">{mensajeEscena}</span>
          <span className="fz-tactical-pct">{progreso}%</span>
        </div>

        <div className="fz-tactical-progress-track">
          <div className="fz-tactical-progress-fill" style={{ width: `${progreso}%` }} />
        </div>

        <button type="button" className="fz-btn-skip-cinematic" onClick={onComplete} title="Saltar animación y acceder ahora">
          Entrar a FutbolZone Directamente ➔
        </button>
      </div>
    </div>
  );
};

export default FutbolLoadingIntro;
