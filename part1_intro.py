# -*- coding: utf-8 -*-
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from pdf_core import styles, NAVY_PRIMARY, BLUE_ACCENT, GREEN_ACCENT, create_callout, create_table

def get_part1_flowables():
    story = []
    
    # ── PORTADA FORMAL ────────────────────────────────────────────────────────
    story.append(Spacer(1, 15))
    story.append(Paragraph("PLAN MAESTRO DE PRUEBAS DE SOFTWARE", styles['CoverTitle']))
    story.append(Paragraph("ESTRATEGIA INTEGRAL DE CALIDAD Y VERIFICACIÓN TÉCNICA BAJO NORMA ISO/IEC/IEEE 29119-3:2021", styles['CoverSubtitle']))
    
    story.append(HRFlowable(width="100%", thickness=2.5, color=GREEN_ACCENT, spaceBefore=0, spaceAfter=15))
    
    callout_cover = (
        "<b>Proyecto Formativo:</b> FutbolZone — Sistema Web Integral de Reserva y Gestión de Canchas Sintéticas<br/>"
        "<b>Programa de Formación:</b> Análisis y Desarrollo de Software (ADSO) — SENA Trimestre III<br/>"
        "<b>Estándar Metodológico:</b> ISO/IEC/IEEE 29119-3:2021 (Software Testing — Test Documentation) y SQRE ISO/IEC 25010<br/>"
        "<b>Nivel de Madurez Evaluado:</b> Producto Mínimo Viable (MVP Operativo) — Alcance Funcional 75.0% Verificado"
    )
    story.append(create_callout(callout_cover, title="DATOS GENERALES DEL PROYECTO", style_type="info"))
    story.append(Spacer(1, 15))
    
    meta_table_data = [
        ["Código Documental:", "PLN-QA-FZ-2026-001", "Versión de la Línea Base:", "1.0 (Oficial)"],
        ["Fecha de Emisión:", "10 de Noviembre de 2026", "Estado del Plan:", "Aprobado para Ejecución"],
        ["Clasificación:", "Técnico / Formativo ADSO", "Entorno Objetivo:", "Local / Staging (FastAPI + React)"],
        ["Elaborado Por:", "Equipo Senior de QA (ADSO)", "Revisado Por:", "Comité Técnico de Desarrollo SENA"],
        ["Repositorio Base:", "FutbolZone-ADSO", "Persistencia Activa:", "SQLite 3.x (futbolzone.db)"],
    ]
    t_meta = create_table(["Atributo", "Valor", "Atributo", "Valor"], meta_table_data, [95, 171, 110, 156])
    story.append(t_meta)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Resumen Ejecutivo:</b> El presente documento formaliza el Plan Maestro de Pruebas para la plataforma web <b>FutbolZone</b>, estableciendo el marco técnico, metodológico y de control de calidad para el ciclo de vida del software. Se define la estrategia de verificación y validación (V&V) aplicable al backend en Python (FastAPI + SQLAlchemy) y frontend en React (TypeScript + Vite), cubriendo autenticación JWT, recuperación por PIN vía Gmail SMTP, motor de reservas sin solapamientos, catálogo de canchas, administración de personal y métricas financieras.", styles['BodyJustified']))
    
    story.append(PageBreak())
    
    # ── TABLA DE CONTENIDO ────────────────────────────────────────────────────
    story.append(Paragraph("TABLA DE CONTENIDO", styles['SectionHeader']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceBefore=0, spaceAfter=8))
    
    toc_data = [
        ["1. Identificación del Documento y Control de Cambios", "3"],
        ["2. Introducción y Contexto del Proyecto", "3"],
        ["3. Propósito del Plan de Pruebas", "3"],
        ["4. Alcance de las Pruebas (Test Scope)", "3"],
        ["5. Objetivos Generales y Específicos de Calidad", "4"],
        ["6. Referencias Documentales y Observación Normativa ISO 29119-3", "4"],
        ["7. Descripción General de la Arquitectura del Sistema", "4"],
        ["8. Componentes y Módulos del Sistema Bajo Prueba", "5"],
        ["9. Funcionalidades Incluidas en el Alcance (In-Scope: 29 HUs)", "5"],
        ["10. Funcionalidades Excluidas o Pendientes (Out-of-Scope: 9 HUs)", "6"],
        ["11. Estrategia y Niveles de Prueba (Pirámide de Pruebas ISO 29119-2)", "7"],
        ["12. Tipos de Pruebas Aplicables al Sistema", "7"],
        ["13. Técnicas de Diseño de Pruebas (ISO/IEC/IEEE 29119-4)", "7"],
        ["14. Entorno de Pruebas, Configuración y Herramientas", "8"],
        ["15. Datos de Prueba y Consideraciones de Seguridad", "8"],
        ["16. Roles, Responsabilidades y Matriz RACI", "9"],
        ["17. Criterios de Entrada (Entry Criteria)", "9"],
        ["18. Criterios de Salida (Exit Criteria)", "9"],
        ["19. Criterios de Suspensión y Reanudación (Approval/Rejection)", "9"],
        ["20. Gestión de Defectos, Ciclo de Vida y Plantilla de Incidencias", "9"],
        ["21. Matriz de Riesgos Técnicos, Funcionales y Mitigación", "10"],
        ["22. Cronograma y Secuencia Metodológica de Actividades", "10"],
        ["23. Entregables del Proceso de Pruebas (Test Deliverables)", "11"],
        ["24. Aprobación del Plan de Pruebas y Firmas Institucionales", "11"],
        ["25. Anexo Técnico: Observaciones Documentales e Inconsistencias", "11"],
    ]
    t_toc = create_table(["Sección del Documento", "Pág."], toc_data, [480, 52], align_cols={1: 'TableCellCenter'})
    story.append(t_toc)
    story.append(PageBreak())
    
    # ── 1. IDENTIFICACIÓN DEL DOCUMENTO ───────────────────────────────────────
    story.append(Paragraph("1. IDENTIFICACIÓN DEL DOCUMENTO", styles['SectionHeader']))
    story.append(Paragraph("El presente documento constituye el Plan Maestro de Pruebas oficial del proyecto FutbolZone, codificado bajo el estándar interno de calidad como <b>PLN-QA-FZ-2026-001</b>. Ha sido estructurado bajo los lineamientos normativos de la norma internacional <b>ISO/IEC/IEEE 29119-3:2021 (Software Testing — Part 3: Test Documentation)</b>.", styles['BodyJustified']))
    
    story.append(Paragraph("1.1 Historial de Control de Cambios", styles['SubsectionHeader']))
    hist_data = [
        ["0.1", "15/08/2026", "Equipo QA ADSO", "Borrador inicial del alcance y definición de módulos core."],
        ["0.5", "01/09/2026", "Líder de Calidad", "Alineación con el Backlog de 38 HUs y justificación del 75%."],
        ["0.9", "15/10/2026", "Líder de Calidad", "Incorporación de hallazgos en código (RBAC, SQLite y Torneos)."],
        ["1.0", "10/11/2026", "Senior QA Lead", "Línea base formal aprobada para ejecución de pruebas integradas."],
    ]
    t_hist = create_table(["Versión", "Fecha", "Autor", "Resumen de Modificaciones"], hist_data, [45, 65, 110, 312], align_cols={0: 'TableCellCenter', 1: 'TableCellCenter'})
    story.append(t_hist)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("1.2 Partes Interesadas y Distribución", styles['SubsectionHeader']))
    dist_data = [
        ["Comité Técnico Evaluador", "Instructores SENA ADSO", "Validación académica y aprobación de entregable de calidad."],
        ["Equipo de Desarrollo Backend", "Ingenieros FastAPI / DB", "Recepción y resolución de defectos de API, ORM y lógica de negocio."],
        ["Equipo de Desarrollo Frontend", "Desarrolladores React SPA", "Corrección de incidencias de UI/UX, integración de API y navegación."],
        ["Aseguramiento de Calidad", "Ingenieros de Prueba QA", "Diseño de casos, ejecución de pruebas, monitoreo y certificación."],
    ]
    t_dist = create_table(["Rol / Audiencia", "Responsable", "Propósito de la Distribución"], dist_data, [130, 130, 272])
    story.append(t_dist)
    story.append(Spacer(1, 10))
    
    # ── 2. INTRODUCCIÓN ───────────────────────────────────────────────────────
    story.append(Paragraph("2. INTRODUCCIÓN", styles['SectionHeader']))
    story.append(Paragraph("En la industria contemporánea del software, el Aseguramiento de Calidad (Software Quality Assurance - SQA) no representa una fase terminal aislada, sino una disciplina continua orientada a la mitigación de riesgos, la validación de requerimientos y la salvaguarda de la integridad de los datos. <b>FutbolZone</b> es una solución web integral diseñada para transformar la gestión comercial y operativa de complejos de canchas sintéticas (Fútbol 5, Fútbol 7 y Fútbol 11), permitiendo la reserva en tiempo real, el cálculo dinámico de tarifas, el control de acceso y la administración global de turnos y personal.", styles['BodyJustified']))
    story.append(Paragraph("Para garantizar que la solución entregada satisfaga los más rigurosos criterios de calidad, este Plan de Pruebas adopta el estándar internacional <b>ISO/IEC/IEEE 29119-3:2021</b> en concordancia con el modelo de características de calidad de software <b>ISO/IEC 25010:2023</b>. La estrategia articula técnicas formales de caja negra y caja blanca para comprobar la adecuación funcional, la confiabilidad de los agendamientos, la seguridad perimetral de los tokens JWT y la compatibilidad visual multiplataforma.", styles['BodyJustified']))
    
    # ── 3. PROPÓSITO DEL PLAN DE PRUEBAS ──────────────────────────────────────
    story.append(Paragraph("3. PROPÓSITO DEL PLAN DE PRUEBAS", styles['SectionHeader']))
    story.append(Paragraph("El propósito fundamental de este documento es definir con precisión técnica el <i>qué</i>, <i>cómo</i>, <i>cuándo</i> y <i>con qué criterios</i> se verificará y validará la plataforma FutbolZone. Este plan busca:", styles['BodyJustified']))
    story.append(Paragraph("• <b>Establecer el Marco Metodológico:</b> Formalizar los niveles, tipos y técnicas de prueba aplicables al código fuente real, evitando suposiciones no sustentadas en artefactos verificables.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Garantizar la Trazabilidad Transversal:</b> Vincular cada Historia de Usuario (HU) del Backlog con sus respectivos endpoints REST en FastAPI, componentes en React, modelos relacionales y casos de prueba.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Descubrir Brechas de Seguridad y Funcionalidad:</b> Identificar de forma temprana vulnerabilidades de control de acceso (RBAC), condiciones de carrera en reservas simultáneas e inconsistencias en la integración cliente-servidor.", styles['BodyBullet']))
    story.append(Paragraph("• <b>Respaldar la Toma de Decisiones:</b> Proporcionar criterios cuantitativos de entrada, salida, suspensión y aceptación para determinar la idoneidad del software frente a una eventual liberación a producción.", styles['BodyBullet']))
    
    # ── 4. ALCANCE DE LAS PRUEBAS (TEST SCOPE) ────────────────────────────────
    story.append(Paragraph("4. ALCANCE DE LAS PRUEBAS (TEST SCOPE)", styles['SectionHeader']))
    story.append(Paragraph("El alcance de este Plan de Pruebas se delimita rigurosamente en función del estado de desarrollo comprobado en el repositorio físico de FutbolZone. Conforme a la matriz oficial <code>Backlog_FutbolZone_Navegable.xlsx</code> y al informe técnico <code>JUSTIFICACION_ALCANCE_75_PORCIENTO.md</code>, el sistema se encuentra en su <b>Fase de Desarrollo del Core Operativo (MVP Funcional al 75.0% de avance)</b>.", styles['BodyJustified']))
    
    callout_alcance = (
        "<b>Delimitación del Alcance Operativo (75.0% Verificado en Código):</b><br/>"
        "• <b>Incluido en el Alcance (In-Scope):</b> 29 Historias de Usuario terminadas correspondientes a Autenticación JWT, Recuperación de clave por PIN Gmail SMTP, Catálogo y Disponibilidad de Canchas, Motor de Reservas sin solapamiento, Dashboard Administrativo, Gestión de Personal (Empleados), Reportes Excel y Dock de Accesibilidad UI (Modo Oscuro/Claro y simulación móvil).<br/>"
        "• <b>Excluido del Alcance (Out-of-Scope):</b> 9 Historias de Usuario en estado 'En Progreso (0%)' del Backlog, incluyendo Pasarela de Pagos (PSE/Wompi), Comprobante PDF descargable con QR, Recordatorios SMS/WhatsApp, Puntos de Fidelización, Sincronización Google Calendar, Brackets de Torneos, Validador QR en portería, Despliegue CI/CD Cloud y Tabla de Auditoría de BD."
    )
    story.append(create_callout(callout_alcance, title="ALCANCE FORMAL DE PRUEBAS DEL MVP", style_type="warning"))
    story.append(Spacer(1, 4))
    
    # ── 5. OBJETIVOS GENERALES Y ESPECÍFICOS DE CALIDAD ───────────────────────
    story.append(Paragraph("5. OBJETIVOS GENERALES Y ESPECÍFICOS DE LA PRUEBA", styles['SectionHeader']))
    story.append(Paragraph("<b>5.1 Objetivo General:</b> Evaluar de manera sistemática, reproducible y trazable la calidad del software FutbolZone conforme a ISO/IEC/IEEE 29119-3, validando la adecuación funcional, la seguridad de acceso, la integridad transaccional y la usabilidad de sus módulos implementados, asegurando que la tasa de defectos críticos sea cero (0) previo al cierre del ciclo.", styles['BodyJustified']))
    story.append(Paragraph("<b>5.2 Objetivos Específicos:</b>", styles['SubsectionHeader']))
    story.append(Paragraph("1. <b>Validar la Seguridad y Autenticación:</b> Certificar el cifrado de contraseñas con Bcrypt, la generación y expiración de tokens JWT (120 min) y la emisión criptográfica de PIN de 6 dígitos con vigencia de 15 min vía SMTP TLS.", styles['BodyBullet']))
    story.append(Paragraph("2. <b>Verificar la Lógica de Disponibilidad y Agendamiento:</b> Comprobar que el motor relacional de reservas impida estrictamente solapamientos horarios en la misma cancha y fecha para estados 'pendiente' y 'confirmada'.", styles['BodyBullet']))
    story.append(Paragraph("3. <b>Evaluar el Algoritmo de Tarifación:</b> Auditar el cálculo automático del costo total: <code>(horas * precio_hora) + kit ($15.000) + árbitro ($30.000) - descuento</code>.", styles['BodyBullet']))
    story.append(Paragraph("4. <b>Inspeccionar la Protección de Rutas (RBAC):</b> Detectar omisiones de dependencias de autorización en endpoints de usuarios y reservas en la API REST de FastAPI.", styles['BodyBullet']))
    story.append(Paragraph("5. <b>Evaluar la Usabilidad y Adaptabilidad del Frontend:</b> Verificar la correcta alternancia de temas (claro/oscuro) y la responsividad tanto en pantalla completa como dentro del mockup interactivo de smartphone.", styles['BodyBullet']))
    story.append(Paragraph("6. <b>Monitorear la Integridad de Persistencia en SQLite:</b> Verificar la consistencia de las restricciones de claves foráneas (<code>PRAGMA foreign_keys=ON</code>) y la ausencia de bloqueos de archivo por escrituras concurrentes.", styles['BodyBullet']))
    
    return story

print("Part 1 defined successfully.")
