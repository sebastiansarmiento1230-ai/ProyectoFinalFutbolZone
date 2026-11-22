# -*- coding: utf-8 -*-
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from pdf_core import styles, NAVY_PRIMARY, BLUE_ACCENT, GREEN_ACCENT, create_callout, create_table

def get_part3_flowables():
    story = []
    
    # ── 11. ESTRATEGIA Y NIVELES DE PRUEBA ────────────────────────────────────
    story.append(Paragraph("11. ESTRATEGIA Y NIVELES DE PRUEBA (ISO/IEC/IEEE 29119-2)", styles['SectionHeader']))
    story.append(Paragraph("La estrategia de pruebas adopta el modelo estandarizado de la <b>Pirámide de Pruebas</b> en consonancia con la norma <b>ISO/IEC/IEEE 29119-2:2021</b>. Este enfoque asegura que la mayor densidad de pruebas se concentre en la base lógica para detectar fallos de manera temprana y a menor costo:", styles['BodyJustified']))
    
    niveles_data = [
        ["Nivel 1: Pruebas Unitarias (Componentes Aislados)", "Lógica de negocio en controladores FastAPI, validadores Pydantic, funciones de hashing Bcrypt, decodificación JWT y helpers de cálculo de tarifas. En frontend: utilitarios de formateo y validadores de formularios.", "Desarrollador / Tester QA", "pytest (Backend), Vitest (Frontend)", "80% de cobertura de controladores core."],
        ["Nivel 2: Pruebas de Integración (API y Contratos)", "Interacción entre endpoints FastAPI y base de datos SQLite mediante SQLAlchemy. Verificación de transacciones, migraciones, restricciones de Foreign Keys y comunicación HTTP fetch cliente-servidor con Bearer tokens.", "Ingeniero QA", "pytest + httpx (TestClient), Postman", "100% de endpoints REST probados con respuestas 200, 400, 401, 403, 422."],
        ["Nivel 3: Pruebas de Sistema (Flujos E2E)", "Validación de flujos completos de usuario extremo a extremo: Registro -> Login -> Exploración -> Reserva -> Verificación en 'Mis Reservas' -> Visualización y cambio de estado en Dashboard Admin.", "Equipo QA", "Playwright / Ejecución Manual Dirigida", "100% de flujos de negocio críticos sin bloqueos operativos."],
        ["Nivel 4: Pruebas de Aceptación (UAT)", "Verificación de los criterios de aceptación Gherkin definidos en el Backlog de Usuario. Validación de experiencia de usuario, modo oscuro, simulación móvil y exportación de reportes Excel.", "Usuarios / Product Owner / Asesor SENA", "Matriz de Criterios de Aceptación", "Aprobación formal del 100% de los criterios del MVP (75%)."],
    ]
    t_niv = create_table(["Nivel de Prueba", "Objetivo y Alcance Técnico", "Responsable", "Herramientas", "Criterio de Cobertura"], niveles_data, [95, 175, 75, 92, 95])
    story.append(t_niv)
    story.append(Spacer(1, 8))
    
    # ── 12. TIPOS DE PRUEBAS APLICABLES ───────────────────────────────────────
    story.append(Paragraph("12. TIPOS DE PRUEBAS APLICABLES AL SISTEMA", styles['SectionHeader']))
    story.append(Paragraph("Se estructuran once (11) tipos de pruebas técnicas especializadas, priorizando los componentes críticos identificados:", styles['BodyJustified']))
    
    tipos_data = [
        ["1. Pruebas Funcionales", "Validar que cada función del sistema responda exactamente a las reglas de negocio descritas en las HUs (ej. registro, creación de reservas, CRUD de canchas y empleados)."],
        ["2. Pruebas de API REST", "Inspección de contratos HTTP: validación de códigos de respuesta (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity), headers CORS y esquemas JSON."],
        ["3. Pruebas de Integración Frontend-Backend", "Verificar la correcta comunicación asíncrona vía fetch: persistencia de tokens en localStorage, renderizado de estados de carga (spinners), captura de errores y alertas visuales de feedback."],
        ["4. Pruebas de Validación de Datos", "Evaluar las restricciones de los esquemas Pydantic: formato estricto de email, longitudes mínimas de contraseña, tipos numéricos positivos en tarifas y validación de formatos de hora HH:MM:SS."],
        ["5. Pruebas de Autenticación y Autorización", "Auditar el ciclo de vida de los tokens JWT: firma criptográfica HMAC-SHA256, expiración tras 120 minutos, rechazo de tokens adulterados o ausentes y protección de rutas privadas."],
        ["6. Pruebas de Roles y Permisos (RBAC)", "Evaluar el aislamiento de privilegios entre rol 'cliente' y 'admin'. Probar acceso no autorizado a rutas administrativas (/api/canchas [POST/PUT/DELETE], /api/empleados, /api/reportes) esperando HTTP 403."],
        ["7. Pruebas de Reservas y Disponibilidad", "Comprobar exhaustivamente la prevención de solapamientos horarios en la misma cancha y fecha: <code>hora_inicio < body.hora_fin AND hora_fin > body.hora_inicio</code> para estados 'pendiente' y 'confirmada'."],
        ["8. Pruebas de Reglas de Negocio", "Auditar el cálculo matemático de tarifas: costo base por duración, recargos de $15.000 por kit deportivo, $30.000 por servicio de arbitraje y aplicación de cupones de descuento promocionales."],
        ["9. Pruebas de Interfaz y Navegación", "Validar la ergonomía visual: comportamiento del acordeón de canchas, filtros interactivos de píldoras, modales emergentes de reserva y login, y navegación fluida sin recargas."],
        ["10. Pruebas de Compatibilidad y Responsividad", "Evaluar el comportamiento del sistema en navegadores modernos (Chrome, Firefox, Edge) y en el conmutador de visualización de ThemeJoystick (Vista Escritorio vs Vista Smartphone)."],
        ["11. Pruebas de Regresión", "Ejecutar suites de verificación tras la corrección de defectos o refactorizaciones para asegurar que los componentes previamente estables no sufran degradación funcional."],
    ]
    t_tip = create_table(["Tipo de Prueba", "Descripción y Alcance de Aplicación en FutbolZone"], tipos_data, [130, 402])
    story.append(t_tip)
    story.append(Spacer(1, 8))
    
    # ── 13. TÉCNICAS DE DISEÑO DE PRUEBAS ──────────────────────────────────────
    story.append(Paragraph("13. TÉCNICAS DE DISEÑO DE PRUEBAS (ISO/IEC/IEEE 29119-4)", styles['SectionHeader']))
    story.append(Paragraph("Conforme a la norma <b>ISO/IEC/IEEE 29119-4:2021</b>, se implementan técnicas formales de diseño para maximizar la detección de defectos con el menor número de casos de prueba:", styles['BodyJustified']))
    
    tecnicas_data = [
        ["Partición de Equivalencias (Equivalence Partitioning)", "División del dominio de entrada en clases válidas e inválidas.<br/>• Formato email: Clase válida ('usuario@dominio.com'), Clases inválidas ('sin_arroba', 'sin_dominio', 'espacios').<br/>• PIN de recuperación: Válido (numérico exacto de 6 dígitos: '123456'), Inválidos (5 dígitos, 7 dígitos, alfanumérico).<br/>• Duración reserva: Válida (>= 1 hora y múltiplos de 30 min), Inválida (< 0 horas, horas invertidas inicio > fin)."],
        ["Análisis de Valores Límite (Boundary Value Analysis)", "Evaluación de casos en las fronteras de decisión del sistema.<br/>• Expiración de PIN: 14 min 59 seg (Aceptado) vs 15 min 01 seg (Rechazado con error 'PIN expirado').<br/>• Cupos de Torneo: 0 equipos (No inicia), max_equipos (Límite lleno), max_equipos + 1 (Inscripción bloqueada).<br/>• Horarios de atención: Límite inferior (06:00:00), Límite superior (23:00:00). Turno fuera de franja (Rechazado)."],
        ["Pruebas de Transición de Estados (State Transition Testing)", "Verificación del ciclo de vida de entidades transaccionales:<br/>• Reserva: [Creada: Pendiente] -> [Abono/Confirmación: Confirmada] -> [Partido Jugado: Completada] ó [Cancelación: Cancelada]. Comprobar que una reserva 'Cancelada' libere el horario para nuevas solicitudes."],
        ["Tablas de Decisión (Decision Table Testing)", "Modelado de combinaciones complejas de tarifas y servicios adicionales:<br/>• Regla 1: Cancha 2h + Sin extras -> Costo = 2 * precio_hora.<br/>• Regla 2: Cancha 1h + Kit ($15.000) -> Costo = precio_hora + 15000.<br/>• Regla 3: Cancha 1h + Kit + Árbitro ($30.000) + Cupón 20% -> Costo = (precio_hora + 45000) * 0.80."],
        ["Pruebas Basadas en Casos de Uso (Use Case Testing)", "Escenarios de negocio completos simulando el comportamiento real de clientes y administradores, cubriendo caminos felices, caminos alternos y manejo de excepciones del sistema."],
    ]
    t_tec = create_table(["Técnica ISO 29119-4", "Aplicación Práctica en FutbolZone y Casos Clave"], tecnicas_data, [130, 402])
    story.append(t_tec)
    story.append(Spacer(1, 8))
    
    # ── 14. ENTORNO DE PRUEBAS Y HERRAMIENTAS ─────────────────────────────────
    story.append(Paragraph("14. ENTORNO DE PRUEBAS Y HERRAMIENTAS (TEST ENVIRONMENT & TOOLS)", styles['SectionHeader']))
    story.append(Paragraph("Para garantizar la repetibilidad y validez de las pruebas, se especifica la configuración de hardware, software y herramental técnico requerido:", styles['BodyJustified']))
    
    env_hw_data = [
        ["Estación de Trabajo de Pruebas", "PC con procesador Intel Core i5/i7 o AMD Ryzen 5/7 (mínimo 4 núcleos, 8 hilos), 16 GB RAM, 256 GB SSD."],
        ["Sistema Operativo del Entorno", "Microsoft Windows 10/11 Pro de 64 bits (PowerShell 7.x / Command Prompt) o Linux Ubuntu 22.04 LTS."],
        ["Conectividad y Red", "Conexión a Internet activa requerida para resolver STARTTLS en puerto 587 contra smtp.gmail.com."],
    ]
    t_hw = create_table(["Componente de Infraestructura", "Especificación Técnica Requerida"], env_hw_data, [140, 392])
    story.append(t_hw)
    story.append(Spacer(1, 4))
    
    tools_data = [
        ["Python 3.14 / 3.11 LTS", "Runtime Backend", "Ejecución del servidor de aplicaciones FastAPI."],
        ["FastAPI 0.111.0 + Uvicorn 0.29", "Framework & Servidor ASGI", "Exposición de endpoints REST y middleware de rutas."],
        ["SQLAlchemy 2.0.30 + SQLite 3.x", "ORM y Persistencia", "Motor de base de datos relacional local en backend/futbolzone.db."],
        ["Node.js 20+ & npm 10+", "Runtime Frontend", "Gestión de paquetes y ejecución de scripts de desarrollo Vite."],
        ["React 19.2.8 + TypeScript 6.0", "Librería SPA UI", "Interfaz web cliente basada en componentes tipados."],
        ["pytest & pytest-asyncio", "Framework de Pruebas Unitarias", "Recomendado para automatización de pruebas de controladores y esquemas."],
        ["httpx (FastAPI TestClient)", "Cliente de Pruebas de API", "Ejecución de llamadas HTTP sintéticas sin levantar servidor de red."],
        ["Postman / Newman v6.x", "Suite de Pruebas de API REST", "Colección automatizada de pruebas de integración y contratos HTTP."],
        ["DB Browser for SQLite v3.12", "Inspección de Persistencia", "Auditoría visual de registros, claves foráneas y estados de base de datos."],
        ["Google Chrome & Firefox DevTools", "Inspección Frontend", "Auditoría de consola, red (pestaña Network), almacenamiento local y responsive."],
    ]
    t_tool = create_table(["Herramienta / Tecnología", "Categoría / Rol", "Propósito en el Proceso de Pruebas"], tools_data, [130, 110, 292])
    story.append(t_tool)
    story.append(Spacer(1, 8))
    
    # ── 15. DATOS DE PRUEBA Y SEGURIDAD ───────────────────────────────────────
    story.append(Paragraph("15. DATOS DE PRUEBA Y CONSIDERACIONES DE SEGURIDAD", styles['SectionHeader']))
    story.append(Paragraph("<b>15.1 Cuentas y Datos Semilla de Prueba:</b> El sistema cuenta con rutinas automáticas de siembra en <code>backend/main.py</code> (función <code>_seed_db()</code>) que garantizan un estado inicial predecible:", styles['BodyJustified']))
    
    seed_data = [
        ["Administrador del Sistema", "admin@futbolzone.com", "admin123", "admin", "Acceso total al Dashboard Admin, Canchas, Reservas y Empleados."],
        ["Cliente Estándar", "cliente@futbolzone.com", "cliente123", "cliente", "Acceso a Mis Reservas, Reserva de Canchas y Calificaciones."],
        ["Usuario de Prueba Gmail Real", "nicolasfelipepazortiz@gmail.com", "admin123", "cliente", "Cuenta vinculada para validación del envío de PIN real por SMTP."],
        ["Canchas Semilla (5 canchas)", "Cancha Central (F5), Norte (F7), Sur (F11), Este (F5), Oeste (F7)", "Tarifas: $45.000 a $100.000 COP", "N/A", "Variedad de capacidades, iluminación y techado para pruebas de filtros."],
        ["Empleados Semilla (5 trabajadores)", "Juan Pérez, María González, Pedro Ramírez, Sofía Torres, Carlos Vargas", "Cargos: Admin, Coordinador, Mantenimiento, Atención, Seguridad", "N/A", "Pruebas de gestión y filtrado de personal laboral."],
    ]
    t_seed = create_table(["Entidad Semilla", "Identificador / Correo", "Contraseña / Tarifas", "Rol", "Propósito de Prueba"], seed_data, [110, 140, 95, 45, 142], align_cols={3: 'TableCellCenter'})
    story.append(t_seed)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>15.2 Consideraciones de Seguridad y Manejo de Información:</b>", styles['SubsectionHeader']))
    story.append(Paragraph("• <b>Aislamiento de Persistencia:</b> Las pruebas destructivas o de carga masiva deben ejecutarse sobre una copia de base de datos dedicada (<code>futbolzone_test.db</code>) para no corromper la base operativa de demostración.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Manejo de Secretos y Credenciales:</b> Se identificó que las contraseñas de aplicación SMTP de Gmail están expuestas en texto claro en <code>backend/.env</code>. Para pruebas en entornos compartidos, se debe ofuscar esta clave y utilizar un servidor SMTP mock (ej. MailHog o Mailpit) para evitar fugas de credenciales personales.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Inyección de Datos Sanitizados:</b> Todo payload de prueba enviado por POST o PUT debe someterse a sanitización contra ataques de inyección SQL y XSS, validando que SQLAlchemy use consultas parametrizadas.", styles['BodyBullet']))
    
    # ── 16. ROLES Y RESPONSABILIDADES (MATRIZ RACI) ────────────────────────────
    story.append(Paragraph("16. ROLES Y RESPONSABILIDADES (MATRIZ RACI)", styles['SectionHeader']))
    story.append(Paragraph("Se define la asignación formal de responsabilidades conforme a la convención <b>RACI</b> (R = Responsible/Responsable, A = Accountable/Aprobador, C = Consulted/Consultado, I = Informed/Informado):", styles['BodyJustified']))
    
    raci_data = [
        ["Diseño y actualización del Plan de Pruebas", "R (Responsable)", "A (Aprobador)", "C (Consultado)", "C (Consultado)", "I (Informado)"],
        ["Diseño y especificación de casos de prueba", "R (Responsable)", "A (Aprobador)", "C (Consultado)", "C (Consultado)", "I (Informado)"],
        ["Configuración del entorno de pruebas y datos", "R (Responsable)", "A (Aprobador)", "R (Responsable)", "R (Responsable)", "I (Informado)"],
        ["Ejecución de pruebas funcionales y de API", "R (Responsable)", "A (Aprobador)", "I (Informado)", "I (Informado)", "I (Informado)"],
        ["Reporte y documentación de defectos", "R (Responsable)", "A (Aprobador)", "I (Informado)", "I (Informado)", "I (Informado)"],
        ["Corrección de defectos en Backend / DB", "I (Informado)", "A (Aprobador)", "R (Responsable)", "I (Informado)", "I (Informado)"],
        ["Corrección de defectos en Frontend / UI", "I (Informado)", "A (Aprobador)", "I (Informado)", "R (Responsable)", "I (Informado)"],
        ["Pruebas de regresión y verificación de fixes", "R (Responsable)", "A (Aprobador)", "C (Consultado)", "C (Consultado)", "I (Informado)"],
        ["Emisión del Informe de Cierre de Pruebas", "R (Responsable)", "A (Aprobador)", "I (Informado)", "I (Informado)", "I (Informado)"],
        ["Aprobación final de liberación del MVP", "C (Consultado)", "R (Responsable)", "C (Consultado)", "C (Consultado)", "A (Aprobador)"],
    ]
    t_raci = create_table(["Actividad de Aseguramiento de Calidad", "Tester QA", "QA Lead", "Dev Backend", "Dev Frontend", "Comité SENA"], raci_data, [160, 74, 74, 74, 74, 76], align_cols={1: 'TableCellCenter', 2: 'TableCellCenter', 3: 'TableCellCenter', 4: 'TableCellCenter', 5: 'TableCellCenter'})
    story.append(t_raci)
    
    return story

print("Part 3 defined successfully.")
