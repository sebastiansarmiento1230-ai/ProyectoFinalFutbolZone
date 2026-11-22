# -*- coding: utf-8 -*-
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from pdf_core import styles, NAVY_PRIMARY, BLUE_ACCENT, GREEN_ACCENT, create_callout, create_table

def get_part2_flowables():
    story = []
    
    # ── 6. REFERENCIAS Y OBSERVACIÓN NORMATIVA ────────────────────────────────
    story.append(Paragraph("6. REFERENCIAS DOCUMENTALES Y OBSERVACIÓN NORMATIVA", styles['SectionHeader']))
    story.append(Paragraph("El diseño, estructuración y terminología de este Plan Maestro de Pruebas se fundamenta en las siguientes fuentes normativas, artefactos de proyecto y código fuente:", styles['BodyJustified']))
    
    ref_data = [
        ["ISO/IEC/IEEE 29119-1:2022", "Software and systems engineering — Software testing — Concepts & definitions", "Estándar Internacional", "Vigente"],
        ["ISO/IEC/IEEE 29119-2:2021", "Software and systems engineering — Software testing — Test processes", "Estándar Internacional", "Vigente"],
        ["ISO/IEC/IEEE 29119-3:2021", "Software and systems engineering — Software testing — Test documentation", "Estándar Internacional", "Consultado (Ref. Canónica)"],
        ["ISO/IEC/IEEE 29119-4:2021", "Software and systems engineering — Software testing — Test techniques", "Estándar Internacional", "Vigente"],
        ["ISO/IEC 25010:2023", "Systems and software engineering — Systems and software Quality Requirements (SQRE)", "Estándar Internacional", "Vigente"],
        ["Backlog_FutbolZone_Navegable.xlsx", "Matriz General de 38 Historias de Usuario, Sprints, Endpoints y Componentes", "Documento del Proyecto", "Disponible en Repositorio"],
        ["Historias_De_Usuario_FutbolZone_ADSO.xlsx", "Matriz de Historias de Usuario de Cliente, Administrador y Resumen Ejecutivo", "Documento del Proyecto", "Disponible en Repositorio"],
        ["JUSTIFICACION_ALCANCE_75_PORCIENTO.md", "Informe Técnico Justificativo de Culminación del MVP Funcional (75.0%)", "Informe Técnico", "Disponible en Repositorio"],
        ["README.md", "Documentación General de Arquitectura, Despliegue y Credenciales de Acceso", "Documento del Repositorio", "Disponible en Repositorio"],
        ["Código Fuente Backend & Frontend", "Rutas FastAPI, Controladores, Modelos SQLAlchemy, Componentes React y Hooks", "Código del Repositorio", "Disponible en Repositorio"],
    ]
    t_ref = create_table(["Identificador / Norma", "Título / Descripción del Documento", "Tipo de Fuente", "Estado"], ref_data, [115, 230, 95, 92])
    story.append(t_ref)
    story.append(Spacer(1, 4))
    
    callout_normativa = (
        "<b>OBSERVACIÓN DOCUMENTAL OBLIGATORIA SOBRE EL ARCHIVO NORMATIVO:</b><br/>"
        "Se deja constancia formal de que el archivo físico denominado <code>ISO-IEC-IEEE-29119-3.pdf</code>, citado en la solicitud de evaluación, <b>no se encontraba adjunto</b> ni dentro de los directorios del proyecto ni en las rutas locales del entorno de trabajo. "
        "En estricto cumplimiento de las directrices éticas y metodológicas de QA de no inventar contenidos documentales inexistentes, este Plan de Pruebas se estructuró a partir de las especificaciones canónicas, plantillas y cláusulas internacionales del estándar <b>ISO/IEC/IEEE 29119-3:2021 (Test Documentation)</b> de conocimiento público y consenso profesional internacional, preservando con fidelidad técnica los 24 apartados requeridos y su nomenclatura estándar."
    )
    story.append(create_callout(callout_normativa, title="DECLARACIÓN DE TRANSPARENCIA NORMATIVA", style_type="warning"))
    story.append(Spacer(1, 8))
    
    # ── 7. DESCRIPCIÓN GENERAL DEL SISTEMA (SYSTEM OVERVIEW) ──────────────────
    story.append(Paragraph("7. DESCRIPCIÓN GENERAL DE LA ARQUITECTURA DEL SISTEMA", styles['SectionHeader']))
    story.append(Paragraph("<b>FutbolZone</b> opera bajo una arquitectura cliente-servidor desacoplada basada en el estilo arquitectural <b>API RESTful</b>. La separación física entre la capa de presentación y la capa de lógica de negocio garantiza la independencia de desarrollo y el consumo mediante clientes web y móviles.", styles['BodyJustified']))
    story.append(Paragraph("• <b>Capa Frontend (SPA Web):</b> Desarrollada con <b>React 19.2.8</b>, <b>TypeScript 6.0</b> y empaquetada mediante <b>Vite 8.2.0</b>. Implementa componentes modulares (CSS individualizado por componente), geolocalización de sedes mediante <b>Leaflet 1.9</b>, exportación local de archivos Excel mediante <b>SheetJS (XLSX 0.18)</b> y un controlador de accesibilidad y viewport (<code>ThemeJoystick.tsx</code>) que permite simular la aplicación dentro del marco de un smartphone interactivo con <i>dynamic island</i> y alternar temas claro y oscuro.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Capa Backend (API REST):</b> Construida en <b>Python 3.14 / 3.11</b> utilizando el framework asíncrono de alto rendimiento <b>FastAPI 0.111.0</b> y servidor ASGI <b>Uvicorn 0.29.0</b>. Implementa esquemas de validación y serialización con <b>Pydantic 2.7.1</b>, middleware global de captura de excepciones (<code>error_handler.py</code>) y configuración CORS abierta (<code>allow_origins=['*']</code>).", styles['BodyBullet']))
    story.append(Paragraph("• <b>Capa de Persistencia y ORM:</b> Utiliza <b>SQLAlchemy 2.0.30</b> como mapeador objeto-relacional (ORM), conectado de forma nativa a un motor <b>SQLite 3.x</b> (<code>backend/futbolzone.db</code>). La integridad referencial se asegura mediante el evento de conexión que ejecuta <code>PRAGMA foreign_keys=ON</code>. El esquema de datos comprende 10 tablas relacionales activas:", styles['BodyBullet']))
    
    db_tables_data = [
        ["usuarios", "id, nombre, apellido, email, telefono, password_hash, rol (admin/cliente), activo, creado_en", "Almacena cuentas de usuario con contraseña cifrada en Bcrypt."],
        ["canchas", "id, nombre, tipo (F5/F7/F11), descripcion, capacidad_jugadores, precio_hora, iluminacion, techo, activa", "Catálogo maestro de canchas deportivas y configuración de tarifas."],
        ["reservas", "id, usuario_id (FK), cancha_id (FK), fecha, hora_inicio, hora_fin, precio_total, estado, notas, creado_en", "Registro transaccional de turnos con estados: pendiente, confirmada, cancelada, completada."],
        ["torneos", "id, nombre, descripcion, cancha_id (FK), categoria, fecha_inicio, fecha_fin, max_equipos, premio, activo", "Definición de campeonatos y copas organizadas por el complejo deportivo."],
        ["inscripciones_torneo", "id, torneo_id (FK), usuario_id (FK), nombre_equipo, creado_en", "Registro de capitanes y equipos inscritos en cada torneo."],
        ["pagos", "id, usuario_id (FK), reserva_id (FK), inscripcion_id (FK), monto, metodo, estado, referencia, creado_en", "Transacciones de recaudo asociadas a reservas (efectivo, transferencia, nequi)."],
        ["horarios", "id, cancha_id (FK), dia, hora_inicio, hora_fin, disponible, creado_en", "Franjas horarias operativas por cancha."],
        ["empleados", "id, nombre, apellido, cargo (Administrador, Coordinador, etc.), telefono, email, activo, creado_en", "Directorio del personal laboral de la sede deportiva."],
        ["resenas", "id, cancha_id (FK), usuario_id (FK), rating (1-5 estrellas), comentario, fecha", "Calificaciones y retroalimentación cualitativa de los clientes."],
        ["password_reset_pins", "id, email, pin (6 dígitos), expira_en (15 min), usado (boolean), creado_en", "Mecanismo criptográfico temporal de recuperación de contraseña."],
    ]
    t_db = create_table(["Tabla Relacional", "Columnas y Restricciones Principales", "Función en el Sistema"], db_tables_data, [95, 240, 197])
    story.append(t_db)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("• <b>Servicios Periféricos de Seguridad y Correo:</b> Autenticación cifrada basada en tokens <b>JWT (JSON Web Tokens)</b> codificados en HMAC-SHA256 (algoritmo HS256) con vigencia configurada de 120 minutos (<code>backend/.env</code>). Servicio de mensajería transaccional real para recuperación de contraseñas configurado mediante <b>SMTP TLS</b> en el puerto 587 a través de los servidores de <b>Google Gmail</b> (<code>smtp.gmail.com</code>).", styles['BodyBullet']))
    
    # ── 8. COMPONENTES Y MÓDULOS BAJO PRUEBA ──────────────────────────────────
    story.append(Paragraph("8. COMPONENTES Y MÓDULOS DEL SISTEMA BAJO PRUEBA", styles['SectionHeader']))
    story.append(Paragraph("A continuación se presenta la matriz técnica de correlación entre los componentes visuales del frontend, los controladores de negocio del backend, los endpoints REST expuestos y su estado de verificación en el repositorio:", styles['BodyJustified']))
    
    modulos_data = [
        ["M01: Autenticación & JWT", "Login.tsx, Registro.tsx", "usuario_controller.py, auth.py", "POST /api/usuarios/registro<br/>POST /api/usuarios/login", "usuarios", "Implementado (100%)"],
        ["M02: Recuperación PIN", "RecuperarPasswordModal.tsx", "password_reset_controller.py", "POST /api/auth/recuperar-password/*", "password_reset_pins", "Implementado (100%)"],
        ["M03: Catálogo Canchas", "Canchas.tsx, AcordeonCanchas.tsx", "cancha_controller.py", "GET /api/canchas/<br/>GET /api/canchas/{id}", "canchas", "Implementado (100%)"],
        ["M04: Disponibilidad", "ReservaCancha.tsx", "cancha_controller.py", "GET /api/canchas/{id}/disponibilidad", "canchas, reservas", "Implementado (100%)"],
        ["M05: Motor Reservas", "ReservaCancha.tsx", "reserva_controller.py", "POST /api/reservas/", "reservas, canchas", "Implementado (100%)"],
        ["M06: Panel Cliente", "DashboardCliente.tsx, TicketReservaModal.tsx", "reserva_controller.py", "GET /api/reservas/mis-reservas<br/>DELETE /api/reservas/{id}", "reservas", "Implementado (100%)"],
        ["M07: Dashboard Admin", "DashboardAdmin.tsx", "cancha_controller.py, empleado_controller.py", "GET/POST/PUT/DELETE /api/canchas/<br/>GET/POST/PUT/DELETE /api/empleados/", "canchas, empleados, reservas", "Implementado (100%)"],
        ["M08: Métricas & Excel", "DashboardAdmin.tsx", "reporte_controller.py, SheetJS", "GET /api/reportes/resumen<br/>Client-side Export", "reservas, pagos", "Implementado (100%)"],
        ["M09: UI Dock & Temas", "ThemeJoystick.tsx, App.tsx", "Client-side (CSS Variables & State)", "N/A (Almacenamiento Local)", "N/A", "Implementado (100%)"],
        ["M10: Reseñas & Feedback", "ResenasModal.tsx", "resena_controller.py", "GET/POST /api/resenas", "resenas", "Implementado (100%)"],
        ["M11: Torneos Deportivos", "TorneosView.tsx", "torneo_controller.py", "GET/POST /api/torneos/<br/>POST /api/torneos/inscribirme", "torneos, inscripciones", "Parcial (Desacoplado)"],
        ["M12: Pasarela Pagos", "PasarelaPago.tsx (Inexistente)", "pago_controller.py (CRUD básico)", "GET/POST /api/pagos/", "pagos", "Pendiente (0%)"],
    ]
    t_mod = create_table(["Módulo Funcional", "Componente Frontend", "Controlador Backend", "Endpoints REST", "Tablas", "Estado en Código"], modulos_data, [95, 105, 100, 120, 52, 60], align_cols={5: 'TableCellCenter'})
    story.append(t_mod)
    story.append(Spacer(1, 8))
    
    # ── 9. FUNCIONALIDADES INCLUIDAS EN EL ALCANCE (IN-SCOPE) ─────────────────
    story.append(Paragraph("9. FUNCIONALIDADES INCLUIDAS EN EL ALCANCE (IN-SCOPE: 29 HUs)", styles['SectionHeader']))
    story.append(Paragraph("El alcance incluye las <b>29 Historias de Usuario verificadas como completadas al 100%</b> en el Backlog del producto y contrastadas contra el código fuente del proyecto:", styles['BodyJustified']))
    
    hus_in_scope = [
        ["HU-01", "Registro de Nuevos Clientes", "Cliente", "5", "POST /api/usuarios/registro", "Validación formato email, password hash con Bcrypt y asignación de rol cliente."],
        ["HU-02", "Inicio de Sesión con JWT", "Todos", "5", "POST /api/usuarios/login", "Emisión de token JWT (120 min), guardado en localStorage y redirección según rol."],
        ["HU-03", "Recuperación Clave PIN Gmail", "Cliente", "8", "POST /api/auth/recuperar-password/*", "PIN de 6 dígitos criptográfico con expiración de 15 min enviado vía Gmail SMTP."],
        ["HU-04", "Catálogo de Canchas", "Todos", "3", "GET /api/canchas/", "Listado de canchas con fotos, tipo (F5, F7, F11), capacidad y precio por hora en COP."],
        ["HU-05", "Filtrado Rápido de Canchas", "Todos", "3", "GET /api/canchas/?tipo=...", "Filtrado reactivo por píldoras de navegación (Todas, F5, F7, F11)."],
        ["HU-06", "Disponibilidad en Tiempo Real", "Cliente", "5", "GET /api/canchas/{id}/disponibilidad", "Consulta dinámica de turnos libres vs ocupados excluyendo fechas pasadas."],
        ["HU-07", "Creación de Reserva", "Cliente", "8", "POST /api/reservas/", "Agendamiento con validación relacional contra solapamientos de turnos."],
        ["HU-08", "Cálculo Automático de Tarifas", "Cliente", "3", "GET /api/canchas/{id}", "Fórmula: (horas * precio_cancha) + kit ($15.000) + árbitro ($30.000) - descuento."],
        ["HU-09", "Panel 'Mis Reservas'", "Cliente", "5", "GET /api/reservas/mis-reservas", "Visualización de reservas personales con badges de estado y detalles de tiquete."],
        ["HU-10", "Cancelación de Reservas", "Cliente", "5", "DELETE /api/reservas/{id}", "Cancelación lógica cambiando estado a 'cancelada' y liberando horario."],
        ["HU-11", "Visualización de Torneos", "Cliente", "5", "GET /api/torneos/", "Consulta de campeonatos y copas (verificado estado mockeado en frontend)."],
        ["HU-12", "Inscripción a Torneos", "Cliente", "5", "POST /api/torneos/inscribirme", "Envío de solicitud de inscripción de equipo (verificado estado local)."],
        ["HU-13", "Dock: Modo Oscuro / Claro", "Todos", "5", "Client-side CSS", "Alternancia de temas con persistencia en localStorage y variables CSS."],
        ["HU-14", "Dock: Modo Celular Interactivo", "Todos", "5", "Client-side Viewport", "Marco visual de smartphone con dynamic island y scroll táctil."],
        ["HU-15", "Dock: Modo Pantalla Completa", "Todos", "5", "Client-side Viewport", "Restauración de ancho fluido de escritorio sin recargar la página."],
        ["HU-21", "Panel Dashboard Admin", "Admin", "8", "GET /api/reportes/resumen", "Métricas en tiempo real: ingresos totales, canchas activas y reservas del mes."],
        ["HU-22", "Métricas Financieras en Vivo", "Admin", "5", "GET /api/reportes/resumen", "KPIs de recaudo discriminados por período (semana, mes, año)."],
        ["HU-23", "Exportación de Reportes a Excel", "Admin", "5", "Client Export (SheetJS)", "Descarga directa de archivos .xlsx con la base de datos de reservas e ingresos."],
        ["HU-24", "Creación de Nuevas Canchas", "Admin", "5", "POST /api/canchas/", "Formulario administrativo con validación de tipo, capacidad, precio y servicios."],
        ["HU-25", "Edición de Tarifas de Canchas", "Admin", "5", "PUT /api/canchas/{id}", "Actualización de precios por hora y características físicas de las canchas."],
        ["HU-26", "Mantenimiento / Desactivación", "Admin", "3", "PUT /api/canchas/{id}", "Deshabilitación temporal (activa=False) para impedir reservas de clientes."],
        ["HU-27", "Eliminación Segura de Canchas", "Admin", "3", "DELETE /api/canchas/{id}", "Baja de canchas con confirmación y verificación de no reservas asociadas."],
        ["HU-28", "Gestión Global de Reservas", "Admin", "5", "GET /api/reservas/", "Listado maestro de reservas de todos los clientes con filtros por estado."],
        ["HU-29", "Cambio de Estado de Reservas", "Admin", "5", "PUT /api/reservas/{id}", "Marcado de reservas como pagadas, completadas o canceladas por el admin."],
        ["HU-30", "Alta de Empleados de Sede", "Admin", "5", "POST /api/empleados/", "Registro de trabajadores (Coordinador, Mantenimiento, Seguridad, Atención)."],
        ["HU-31", "Listado y Edición de Personal", "Admin", "3", "GET/PUT /api/empleados/{id}", "Actualización de cargo, teléfono y datos de contacto de empleados."],
        ["HU-32", "Activación/Desactivación Staff", "Admin", "3", "PUT /api/empleados/{id}", "Bloqueo de personal inactivo conservando trazabilidad histórica."],
        ["HU-33", "Creación de Nuevos Torneos", "Admin", "5", "POST /api/torneos/", "Apertura de campeonatos con cupo máximo, precio de inscripción y premio."],
        ["HU-34", "Protección de Rutas RBAC", "Admin", "5", "Middleware Auth JWT", "Control de acceso para rechazar a usuarios sin token o con rol no admin."],
    ]
    t_in = create_table(["ID", "Historia de Usuario", "Rol", "Pts", "Endpoint / Mecanismo", "Criterio Clave a Validar"], hus_in_scope, [32, 115, 45, 22, 128, 190], align_cols={0: 'TableCellCenter', 2: 'TableCellCenter', 3: 'TableCellCenter'})
    story.append(t_in)
    story.append(Spacer(1, 8))
    
    # ── 10. FUNCIONALIDADES EXCLUIDAS (OUT-OF-SCOPE) ───────────────────────────
    story.append(Paragraph("10. FUNCIONALIDADES EXCLUIDAS O PENDIENTES (OUT-OF-SCOPE: 9 HUs)", styles['SectionHeader']))
    story.append(Paragraph("Las siguientes <b>9 Historias de Usuario se encuentran en estado 'En Progreso (0%)'</b> en el Backlog oficial. Su exclusión técnica del presente plan responde a que sus componentes y dependencias externas aún no existen en el código fuente actual, estando programadas para la Fase de Escalabilidad (Trimestre IV):", styles['BodyJustified']))
    
    hus_out_scope = [
        ["HU-16", "Pasarela de Pagos Online PSE / Wompi", "Cliente", "Pagos", "8", "No implementado. No existen credenciales de pasarela ni webhooks bancarios en el backend."],
        ["HU-17", "Comprobante PDF Descargable con QR", "Cliente", "Comprobantes", "5", "No implementado. No existe librería ReportLab/FPDF en backend ni componente ComprobanteReserva.tsx."],
        ["HU-18", "Notificaciones SMS / WhatsApp", "Cliente", "Notificaciones", "5", "No implementado. No existe integración con API de Twilio ni Meta Cloud API en el código."],
        ["HU-19", "Sistema de Puntos y Fidelización", "Cliente", "Fidelización", "3", "No implementado. No existe modelo relacional ni endpoints para acumulación de puntos."],
        ["HU-20", "Sincronización con Google Calendar", "Cliente", "Integraciones", "3", "No implementado. No existe integración con Google Calendar API v3 ni OAuth de calendario."],
        ["HU-35", "Generador Automático de Brackets", "Admin", "Torneos", "5", "No implementado. El sorteo automático de eliminatorias no existe en el controlador."],
        ["HU-36", "Validador de QR en Portería", "Admin", "Seguridad", "5", "No implementado. No existe interfaz de cámara web ni componente de lectura QR."],
        ["HU-37", "Despliegue Continuo Cloud (CI/CD)", "Admin", "DevOps", "8", "No implementado. No existen Dockerfile, docker-compose.yml ni GitHub Actions."],
        ["HU-38", "Módulo de Auditoría y Logs de BD", "Admin", "Seguridad", "3", "No implementado. No existe tabla de auditoría de transacciones en la base de datos."],
    ]
    t_out = create_table(["ID", "Historia de Usuario", "Rol", "Módulo", "Pts", "Justificación Técnica de la Exclusión"], hus_out_scope, [32, 130, 45, 65, 22, 238], align_cols={0: 'TableCellCenter', 2: 'TableCellCenter', 4: 'TableCellCenter'})
    story.append(t_out)
    
    return story

print("Part 2 defined successfully.")
