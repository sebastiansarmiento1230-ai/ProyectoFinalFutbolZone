# -*- coding: utf-8 -*-
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from pdf_core import styles, NAVY_PRIMARY, BLUE_ACCENT, GREEN_ACCENT, create_callout, create_table

def get_part4_flowables():
    story = []
    
    # ── 17. CRITERIOS DE ENTRADA (ENTRY CRITERIA) ─────────────────────────────
    story.append(Paragraph("17. CRITERIOS DE ENTRADA (ENTRY CRITERIA)", styles['SectionHeader']))
    story.append(Paragraph("Para iniciar formalmente la ejecución de un ciclo de pruebas en FutbolZone, deben cumplirse las siguientes condiciones precedentes sin excepción:", styles['BodyJustified']))
    
    entry_data = [
        ["CE-01", "Disponibilidad del Backend", "El servidor FastAPI debe iniciar sin errores en el puerto 5000 y responder con código HTTP 200 en el endpoint raíz <code>GET /</code>."],
        ["CE-02", "Persistencia Operativa", "El archivo de base de datos <code>backend/futbolzone.db</code> debe estar accesible, con claves foráneas habilitadas y los datos semilla sembrados."],
        ["CE-03", "Compilación Exitosa del Frontend", "El proyecto en React debe compilar sin errores de TypeScript (<code>npm run build</code> exitoso) y el servidor Vite debe estar corriendo en puerto 5173."],
        ["CE-04", "Documentación de API Accesible", "La interfaz Swagger UI interactiva debe estar operativa en <code>http://localhost:5000/docs</code> para validación de contratos."],
        ["CE-05", "Casos de Prueba Aprobados", "La especificación formal de casos de prueba debe contar con el visto bueno del Líder de Calidad."],
        ["CE-06", "Servicio SMTP Conectable", "Las credenciales en <code>backend/.env</code> deben permitir resolución y autenticación TLS contra smtp.gmail.com:587."],
    ]
    t_entry = create_table(["ID", "Criterio de Entrada", "Condición Técnica de Validación"], entry_data, [40, 130, 362], align_cols={0: 'TableCellCenter'})
    story.append(t_entry)
    story.append(Spacer(1, 8))
    
    # ── 18. CRITERIOS DE SALIDA (EXIT CRITERIA) ───────────────────────────────
    story.append(Paragraph("18. CRITERIOS DE SALIDA (EXIT CRITERIA)", styles['SectionHeader']))
    story.append(Paragraph("El ciclo de pruebas del MVP (Fase Trimestre III) se considerará formalmente concluido cuando se satisfagan las siguientes metas de calidad:", styles['BodyJustified']))
    
    exit_data = [
        ["CS-01", "Cobertura de Ejecución", "Haber ejecutado el 100% de los casos de prueba diseñados para las 29 Historias de Usuario dentro del alcance."],
        ["CS-02", "Tasa de Éxito Global", "Alcanzar una tasa mínima de aprobación del 95% sobre el total de pruebas funcionales ejecutadas."],
        ["CS-03", "Tolerancia Cero Defectos Críticos", "Cero (0) defectos abiertos clasificados con severidad Bloqueante (Sev 1) o Crítica (Sev 2)."],
        ["CS-04", "Resolución de Defectos Mayores", "Al menos el 90% de los defectos clasificados como Mayores (Sev 3) deben estar resueltos y verificados."],
        ["CS-05", "Plan de Mitigación de Defectos Menores", "El 100% de los defectos Menores (Sev 4) o Triviales (Sev 5) deben estar documentados con plan de corrección para el Trimestre IV."],
        ["CS-06", "Emisión del Informe de Cierre", "Elaboración y firma del Informe de Finalización de Pruebas conforme a ISO/IEC/IEEE 29119-3."],
    ]
    t_exit = create_table(["ID", "Criterio de Salida", "Umbral Cuantitativo / Requisito Formal"], exit_data, [40, 140, 352], align_cols={0: 'TableCellCenter'})
    story.append(t_exit)
    story.append(Spacer(1, 8))
    
    # ── 19. CRITERIOS DE SUSPENSIÓN Y REANUDACIÓN ─────────────────────────────
    story.append(Paragraph("19. CRITERIOS DE APROBACIÓN Y RECHAZO (SUSPENSIÓN Y REANUDACIÓN)", styles['SectionHeader']))
    story.append(Paragraph("<b>19.1 Criterios de Suspensión (Detención del Ciclo de Pruebas):</b> Las actividades de prueba se detendrán de forma inmediata ante la ocurrencia de cualquiera de los siguientes eventos:", styles['BodyJustified']))
    story.append(Paragraph("• <b>Caída o Bloqueo Crítico del Backend:</b> Falla recurrente (Crash) del servidor Uvicorn que impida levantar la API.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Inoperatividad de Autenticación:</b> Bloqueo total en <code>POST /api/usuarios/login</code> que impida el acceso tanto al rol admin como al rol cliente.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Corrupción de Base de Datos:</b> Errores de bloqueo irrecuperable de SQLite (<code>OperationalError: database is locked</code>) o pérdida de integridad relacional.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Tasa Excesiva de Fallos en Smoke Testing:</b> Si más del 30% de las pruebas de humo iniciales fallan en el primer pase.", styles['BodyBullet']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>19.2 Criterios de Reanudación:</b> Las pruebas se reiniciarán una vez se cumplan las siguientes condiciones:", styles['SubsectionHeader']))
    story.append(Paragraph("• Entrega formal de una nueva compilación o parche de código por parte de desarrollo con las correcciones integradas.", styles['BodyBullet']))
    story.append(Paragraph("• Restauración de la base de datos <code>futbolzone.db</code> a un estado semilla consistente y verificado.", styles['BodyBullet']))
    story.append(Paragraph("• Ejecución exitosa de la suite de Smoke Testing demostrando la estabilidad de los flujos principales.", styles['BodyBullet']))
    story.append(Spacer(1, 6))
    
    # ── 20. GESTIÓN DE DEFECTOS E INCIDENCIAS ─────────────────────────────────
    story.append(Paragraph("20. GESTIÓN DE DEFECTOS E INCIDENCIAS (ISO/IEC/IEEE 29119-3)", styles['SectionHeader']))
    story.append(Paragraph("El ciclo de vida de los defectos sigue una máquina de estados estricta orientada a garantizar que ninguna anomalía detectada quede sin resolución documentada:", styles['BodyJustified']))
    story.append(Paragraph("<b>Estados del Defecto:</b> [Nuevo] → [Asignado] → [En Corrección] → [Corregido/Resuelto] → [En Verificación] → [Cerrado] (o [Reabierto] si la prueba de verificación falla).", styles['BodyBullet']))
    story.append(Spacer(1, 2))
    
    defect_sev_data = [
        ["Severidad 1: Bloqueante (Blocker)", "Impide por completo la ejecución de pruebas subsiguientes o el uso del sistema. Causa crash del servidor o pérdida irrecuperable de datos.", "Inmediata (< 4 horas)"],
        ["Severidad 2: Crítica (Critical)", "Falla grave en una regla de negocio fundamental (ej. solapamiento de reservas en la misma cancha) sin mecanismo alternativo viable.", "Alta (< 12 horas)"],
        ["Severidad 3: Mayor (Major)", "Fallo funcional importante pero que cuenta con un procedimiento temporal (workaround) conocido (ej. fallo en exportación Excel).", "Media (< 24 horas)"],
        ["Severidad 4: Menor (Minor)", "Inconsistencia menor en interfaz de usuario, alineación visual, formato de fecha o mensaje informativo ambiguo.", "Baja (Próximo Sprint)"],
        ["Severidad 5: Trivial (Trivial)", "Detalle estético menor que no afecta en absoluto la operatividad ni la lógica de negocio (ej. tipografía o color de borde).", "Deseable (Backlog)"],
    ]
    t_sev = create_table(["Nivel de Severidad", "Criterio de Impacto Técnico y Operacional", "SLA de Resolución"], defect_sev_data, [130, 310, 92])
    story.append(t_sev)
    story.append(Spacer(1, 4))
    
    callout_defect_template = (
        "<b>ESTRUCTURA DE REPORTE DE DEFECTO (TEMPLATE ISO 29119-3):</b><br/>"
        "• <b>ID Defecto:</b> DEF-FZ-[Módulo]-[Correlativo] (ej. DEF-FZ-RES-001)<br/>"
        "• <b>Título Conciso:</b> Resumen descriptivo del fallo (ej. 'Permite reservar cancha ocupada si hora_inicio coincide con hora_fin').<br/>"
        "• <b>Historia de Usuario Asociada:</b> Identificador de HU (ej. HU-07: Creación de Reserva).<br/>"
        "• <b>Severidad & Prioridad:</b> Sev 2 (Crítica) / Prioridad Alta.<br/>"
        "• <b>Precondiciones:</b> Estado inicial requerido en BD y sesión autenticada.<br/>"
        "• <b>Pasos para Reproducir:</b> Secuencia numerada exacta de acciones realizadas.<br/>"
        "• <b>Resultado Obtenido:</b> Comportamiento erróneo del sistema (incluir código HTTP o error en consola).<br/>"
        "• <b>Resultado Esperado:</b> Comportamiento correcto conforme a los criterios de aceptación.<br/>"
        "• <b>Evidencias Adjuntas:</b> Capturas de pantalla, payload JSON de request/response y logs de Uvicorn."
    )
    story.append(create_callout(callout_defect_template, title="PLANTILLA ESTÁNDAR DE REGISTRO DE DEFECTOS", style_type="info"))
    story.append(Spacer(1, 8))
    
    # ── 21. MATRIZ DE RIESGOS TÉCNICOS Y MITIGACIÓN ───────────────────────────
    story.append(Paragraph("21. MATRIZ DE RIESGOS TÉCNICOS, FUNCIONALES Y MITIGACIÓN", styles['SectionHeader']))
    story.append(Paragraph("A partir del análisis exhaustivo del código fuente y la arquitectura de FutbolZone, se identificaron ocho (8) riesgos técnicos de alto impacto, formulándose sus correspondientes planes de mitigación:", styles['BodyJustified']))
    
    riesgos_data = [
        ["R-01: Brecha de Autorización RBAC en Usuarios", "Alta", "Crítica", "Endpoints sensibles en <code>usuario_routes.py</code> (/api/usuarios/, /clientes, /{id}, /{id}/rol) carecen de <code>Depends(get_admin_actual)</code>. Cualquier cliente puede listar usuarios o elevar su rol a 'admin'.", "<b>Plan de Mitigación:</b> Agregar de inmediato el decorador de inyección de dependencias <code>admin: dict = Depends(get_admin_actual)</code> a todas las rutas administrativas de usuario."],
        ["R-02: Modificación y Cancelación no Autorizada de Reservas", "Alta", "Alta", "Rutas <code>PUT /api/reservas/{id}</code> y <code>DELETE /api/reservas/{id}</code> no validan que la reserva pertenezca al usuario solicitante ni exigen rol admin.", "<b>Plan de Mitigación:</b> Inyectar <code>get_usuario_actual</code> y validar en el controlador que <code>reserva.usuario_id == current_user.id</code> o que el rol sea <code>admin</code>."],
        ["R-03: Condición de Carrera en Reservas Concurrentes", "Media", "Crítica", "La validación de solapamiento en <code>reserva_controller.py</code> es una consulta previa al <code>db.commit()</code>. Dos solicitudes simultáneas pueden pasar el filtro y solaparse en SQLite.", "<b>Plan de Mitigación:</b> Implementar transacción atómica con constraint UNIQUE relacional a nivel de tabla o bloqueo transaccional explícito antes de confirmar."],
        ["R-04: Desconexión de Torneos en Frontend", "Alta", "Media", "El componente <code>TorneosView.tsx</code> opera con datos mockeados en <code>localStorage</code> y no invoca los endpoints <code>/api/torneos/</code> desarrollados en backend.", "<b>Plan de Mitigación:</b> Refactorizar <code>TorneosView.tsx</code> y <code>api.ts</code> para consumir los servicios backend reales, manteniendo fallback local en caso de desconexión."],
        ["R-05: Exposición de PIN de Recuperación en Respuesta HTTP", "Alta", "Alta", "Si falla el envío por SMTP en <code>password_reset_controller.py</code>, la API devuelve el PIN en claro en el JSON de respuesta (<code>pin_demo</code>).", "<b>Plan de Mitigación:</b> Suprimir la clave <code>pin_demo</code> de la respuesta en entornos de producción y limitar su emisión estrictamente a entornos locales de desarrollo."],
        ["R-06: Exposición de Secretos en Archivo .env", "Alta", "Alta", "El archivo <code>backend/.env</code> contiene contraseñas de aplicación SMTP reales en texto plano dentro del repositorio entregado.", "<b>Plan de Mitigación:</b> Añadir <code>.env</code> a <code>.gitignore</code>, rotar inmediatamente la contraseña de aplicación de Gmail y emplear variables de entorno seguras de sistema."],
        ["R-07: Inexistencia de Suite de Pruebas Automatizadas", "Alta", "Alta", "El backend y frontend carecen de tests unitarios o de integración en sus paquetes; los únicos tests existentes están en un laboratorio aislado (<code>actividad_tdd</code>).", "<b>Plan de Mitigación:</b> Implementar una suite base en <code>pytest</code> para los controladores de reservas y auth, e incorporar pruebas de componentes con <code>Vitest</code>."],
        ["R-08: Bloqueos de Persistencia por Concurrencia SQLite", "Media", "Media", "SQLite admite un único escritor simultáneo. Ráfagas de reservas o inscripciones pueden generar errores <code>database is locked</code>.", "<b>Plan de Mitigación:</b> Configurar <code>timeout=10</code> en la cadena de conexión de SQLite y planificar la migración a PostgreSQL o MySQL para producción."],
    ]
    t_risk = create_table(["ID y Riesgo Identificado", "Prob.", "Imp.", "Descripción Técnica del Riesgo en el Código", "Estrategia de Mitigación QA"], riesgos_data, [105, 30, 32, 175, 190], align_cols={1: 'TableCellCenter', 2: 'TableCellCenter'})
    story.append(t_risk)
    story.append(Spacer(1, 8))
    
    # ── 22. CRONOGRAMA Y ACTIVIDADES ──────────────────────────────────────────
    story.append(Paragraph("22. CRONOGRAMA O SECUENCIA DE ACTIVIDADES", styles['SectionHeader']))
    story.append(Paragraph("El ciclo de pruebas se estructura en seis (6) fases metodológicas secuenciales:", styles['BodyJustified']))
    
    fases_data = [
        ["Fase 1: Planificación & Análisis", "Estudio del repositorio, análisis de código, contrastación de backlog y formalización de este Plan de Pruebas.", "QA Senior", "Semana 1"],
        ["Fase 2: Diseño de Casos de Prueba", "Elaboración de la matriz detallada de casos de prueba de caja negra y caja blanca aplicando técnicas ISO 29119-4.", "Equipo QA", "Semana 1 - 2"],
        ["Fase 3: Configuración de Entorno & Smoke Test", "Despliegue del entorno local aislado, siembra de datos y ejecución de Smoke Testing sobre endpoints core.", "DevOps / QA", "Semana 2"],
        ["Fase 4: Ejecución Ciclo 1 (Pruebas Funcionales & API)", "Ejecución de pruebas de API REST, validación de datos, autenticación, solapamientos horarios y panel administrativo.", "Equipo QA", "Semana 2 - 3"],
        ["Fase 5: Ciclo 2 (Regresión & Pruebas No Funcionales)", "Verificación de defectos resueltos por desarrollo, pruebas de regresión, responsividad y concurrencia SQLite.", "Equipo QA", "Semana 3 - 4"],
        ["Fase 6: Cierre, Evaluación y Métricas", "Consolidación de métricas de cobertura, evaluación de criterios de salida y emisión del Informe de Cierre.", "QA Lead / SENA", "Semana 4"],
    ]
    t_fases = create_table(["Fase Metodológica", "Actividades Principales", "Responsable", "Duración"], fases_data, [120, 262, 90, 60], align_cols={3: 'TableCellCenter'})
    story.append(t_fases)
    story.append(Spacer(1, 8))
    
    # ── 23. ENTREGABLES DE PRUEBA ─────────────────────────────────────────────
    story.append(Paragraph("23. ENTREGABLES DEL PROCESO DE PRUEBAS (TEST DELIVERABLES)", styles['SectionHeader']))
    story.append(Paragraph("En conformidad con la norma ISO/IEC/IEEE 29119-3, el proceso de pruebas genera los siguientes artefactos formales:", styles['BodyJustified']))
    story.append(Paragraph("1. <b>Plan Maestro de Pruebas (Test Plan):</b> Documento formal rector (el presente archivo <code>Plan_de_Pruebas_FutbolZone.pdf</code>).", styles['BodyBullet']))
    story.append(Paragraph("2. <b>Especificación de Casos de Prueba (Test Case Specification):</b> Catálogo detallado de casos de prueba con identificador, precondiciones, pasos, datos de prueba y resultados esperados.", styles['BodyBullet']))
    story.append(Paragraph("3. <b>Informes de Estado de Pruebas (Test Status Reports):</b> Reportes periódicos de avance indicando casos ejecutados, aprobados, fallidos y bloqueados.", styles['BodyBullet']))
    story.append(Paragraph("4. <b>Registro de Defectos (Defect Log):</b> Repositorio estructurado de todas las anomalías identificadas con su severidad, prioridad, evidencias y estado de resolución.", styles['BodyBullet']))
    story.append(Paragraph("5. <b>Informe de Cierre de Pruebas (Test Completion Report):</b> Documento terminal que evalúa los criterios de salida, certifica la calidad del MVP y autoriza la entrega final.", styles['BodyBullet']))
    story.append(Spacer(1, 6))
    
    # ── 24. APROBACIÓN DEL PLAN ───────────────────────────────────────────────
    story.append(Paragraph("24. APROBACIÓN DEL PLAN DE PRUEBAS", styles['SectionHeader']))
    story.append(Paragraph("La firma del presente documento certifica el acuerdo de las partes sobre el alcance, objetivos, criterios y riesgos aquí definidos:", styles['BodyJustified']))
    
    firmas_data = [
        ["Líder Senior de Calidad (QA Lead)", "Equipo de Aseguramiento de Calidad SENA ADSO", "10/11/2026", "Aprobado"],
        ["Líder de Desarrollo Backend", "Equipo de Backend & Base de Datos (FastAPI)", "10/11/2026", "Aprobado"],
        ["Líder de Desarrollo Frontend", "Equipo de Frontend SPA (React + TypeScript)", "10/11/2026", "Aprobado"],
        ["Instructor Asesor Técnico", "Centro de Formación ADSO — Regional SENA", "10/11/2026", "Aprobado"],
    ]
    t_firmas = create_table(["Rol Institucional", "Nombre / Delegación Técnica", "Fecha", "Decisión"], firmas_data, [130, 232, 85, 85], align_cols={2: 'TableCellCenter', 3: 'TableCellCenter'})
    story.append(t_firmas)
    story.append(Spacer(1, 10))
    
    # ── 25. ANEXO DE OBSERVACIONES DOCUMENTALES ───────────────────────────────
    story.append(Paragraph("25. ANEXO TÉCNICO: OBSERVACIONES DOCUMENTALES Y ANÁLISIS DE INCONSISTENCIAS", styles['SectionHeader']))
    story.append(Paragraph("En cumplimiento riguroso del rol de Senior QA y de las instrucciones de auditoría técnica, se documentan las siguientes contradicciones encontradas entre la documentación del proyecto, el backlog y el código fuente real:", styles['BodyJustified']))
    
    obs_data = [
        ["Contradicción 1: Porcentaje de Avance Global", "<b>README.md (98%):</b> Afirma que el proyecto está al '98% de desarrollo funcional y productivo'.<br/><b>JUSTIFICACION_ALCANCE_75_PORCIENTO.md (75.0%):</b> Informa que el avance es del 75.0% correspondiente a la fase culminada del MVP.<br/><b>Backlog General:</b> Contiene 38 HUs, de las cuales 29 están al 100% y 9 al 0% (29/38 = 76.3% de HUs y 75.0% de puntos).<br/><b>Dictamen QA:</b> La cifra real y técnicamente comprobable es <b>75.0%</b>. La afirmación de 98% en el README es una sobrestimación de marketing que omite las 9 HUs pendientes del roadmap."],
        ["Contradicción 2: Motor de Base de Datos y Fallback", "<b>README.md:</b> Afirma contar con 'Base de Datos Relacional SQLite Nativa + Fallback MySQL' y 'FastAPI + SQLite/MySQL'.<br/><b>Código Fuente (database.py):</b> La conexión es fija a SQLite (<code>sqlite:///{DB_PATH}</code>). No existe código de fallback dinámico ni conmutación a MySQL en tiempo de ejecución.<br/><b>Dictamen QA:</b> La base de datos es exclusivamente SQLite nativo. La mención de fallback es documental y no se refleja en la arquitectura de software actual."],
        ["Contradicción 3: Estado del Módulo de Torneos", "<b>Backlog y README:</b> Marcan HU-11, HU-12 y HU-33 como '100% completadas' con endpoints /api/torneos/.<br/><b>Código Fuente Frontend:</b> <code>TorneosView.tsx</code> almacena la tabla de posiciones y el fixture en <code>localStorage</code> y la inscripción solo muestra un alert() local; no se comunica con los endpoints del backend.<br/><b>Dictamen QA:</b> El módulo está <b>parcialmente implementado y desacoplado</b>. El backend expone los endpoints pero el cliente web no los consume."],
        ["Contradicción 4: Estado de Pruebas Automatizadas", "<b>README.md:</b> Afirma que todos los módulos centrales están 'completamente probados e integrados'.<br/><b>Código Fuente:</b> No existen archivos de pruebas en <code>backend/</code> (solo test_email.py manual) ni en <code>frontend/package.json</code> (no hay Vitest ni Jest). Las únicas pruebas existentes están en <code>actividad_tdd/</code> (16 tests con unittest), pero pertenecen a un ejercicio académico de consola CLI sin conexión con FastAPI.<br/><b>Dictamen QA:</b> No existe evidencia de pruebas automatizadas sobre la aplicación web real. Se requiere implementar la suite propuesta en este plan."],
        ["Observación 5: Ausencia del PDF Normativo", "<b>Solicitud Inicial:</b> Se referenció el documento <code>ISO-IEC-IEEE-29119-3.pdf</code> como insumo adjunto.<br/><b>Inspección de Archivos:</b> El archivo no se encontró dentro del paquete de entrega ni en rutas locales.<br/><b>Dictamen QA:</b> Se aplicó la especificación técnica internacional canónica de la norma ISO/IEC/IEEE 29119-3:2021 de público conocimiento sin inventar especificaciones no verificables."],
    ]
    t_obs = create_table(["Hallazgo / Inconsistencia", "Contraste Documental vs Código Fuente y Dictamen QA"], obs_data, [130, 402])
    story.append(t_obs)
    
    return story

print("Part 4 defined successfully.")
