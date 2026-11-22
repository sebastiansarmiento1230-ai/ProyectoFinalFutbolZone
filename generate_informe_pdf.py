# -*- coding: utf-8 -*-
"""
Script: generate_informe_pdf.py
Genera: Informe_Ejecucion_Pruebas_FutZone.pdf
Norma: ISO/IEC/IEEE 29119-3:2021
"""
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

# ─── CONSTANTES DE MARCA ────────────────────────────────────────────────────
NAVY     = colors.HexColor("#1B365D")
TEAL     = colors.HexColor("#0E7490")
SLATE    = colors.HexColor("#2C3E50")
PASS_G   = colors.HexColor("#166534")
FAIL_R   = colors.HexColor("#991B1B")
AMBER    = colors.HexColor("#92400E")
GRAY_LT  = colors.HexColor("#F8FAFC")
GRAY_MID = colors.HexColor("#E2E8F0")
GRAY_TXT = colors.HexColor("#475569")
WHITE    = colors.white
BLACK    = colors.HexColor("#0F172A")

PASS_BG  = colors.HexColor("#DCFCE7")
FAIL_BG  = colors.HexColor("#FEE2E2")
NOEX_BG  = colors.HexColor("#F1F5F9")
NOAP_BG  = colors.HexColor("#FEF3C7")
HEADER_BG= colors.HexColor("#1B365D")
SUBHDR_BG= colors.HexColor("#E2E8F0")

FECHA_INFORME = "10 de noviembre de 2026"
VERSION       = "1.0"
OUTPUT_FILE   = "Informe_Ejecucion_Pruebas_FutZone.pdf"

# ─── ESTILOS ────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S("CoverTitle", fontName="Helvetica-Bold", fontSize=28,
                textColor=WHITE, alignment=TA_CENTER, leading=34)
cover_sub   = S("CoverSub",   fontName="Helvetica-Bold", fontSize=16,
                textColor=colors.HexColor("#93C5FD"), alignment=TA_CENTER, leading=22)
cover_meta  = S("CoverMeta",  fontName="Helvetica",      fontSize=11,
                textColor=colors.HexColor("#CBD5E1"), alignment=TA_CENTER, leading=16)

h1 = S("H1", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,
        spaceBefore=18, spaceAfter=6, leading=20)
h2 = S("H2", fontName="Helvetica-Bold", fontSize=12, textColor=TEAL,
        spaceBefore=14, spaceAfter=4, leading=16)
h3 = S("H3", fontName="Helvetica-Bold", fontSize=10.5, textColor=SLATE,
        spaceBefore=10, spaceAfter=3, leading=14)
body = S("Body", fontName="Helvetica", fontSize=9.5, textColor=BLACK,
         leading=14, spaceAfter=4, alignment=TA_JUSTIFY)
body_bullet = S("BodyBullet", fontName="Helvetica", fontSize=9.5, textColor=BLACK,
                leading=14, spaceAfter=3, leftIndent=12, firstLineIndent=-12)
note_style = S("Note", fontName="Helvetica-Oblique", fontSize=8.5,
               textColor=GRAY_TXT, leading=12, spaceAfter=4)
bold_body  = S("BoldBody", fontName="Helvetica-Bold", fontSize=9.5, textColor=BLACK,
               leading=14, spaceAfter=4)
cell_style = S("Cell", fontName="Helvetica", fontSize=8, textColor=BLACK,
               leading=11, spaceAfter=0)
cell_bold  = S("CellBold", fontName="Helvetica-Bold", fontSize=8, textColor=BLACK,
               leading=11, spaceAfter=0)
cell_pass  = S("CellPass", fontName="Helvetica-Bold", fontSize=8, textColor=PASS_G,
               leading=11, alignment=TA_CENTER)
cell_fail  = S("CellFail", fontName="Helvetica-Bold", fontSize=8, textColor=FAIL_R,
               leading=11, alignment=TA_CENTER)
cell_noex  = S("CellNoex", fontName="Helvetica", fontSize=8, textColor=GRAY_TXT,
               leading=11, alignment=TA_CENTER)
cell_noap  = S("CellNoap", fontName="Helvetica-Bold", fontSize=8, textColor=AMBER,
               leading=11, alignment=TA_CENTER)

toc_style  = S("TOC",  fontName="Helvetica", fontSize=10, textColor=NAVY,
               leading=16, spaceAfter=2)
toc_sub    = S("TOCSub",fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY_TXT,
               leading=14, spaceAfter=1, leftIndent=14)

# ─── HELPERS ────────────────────────────────────────────────────────────────
def P(text, style=None):
    return Paragraph(text, style or body)

def hr(color=GRAY_MID, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=4)

def SP(h=0.25):
    return Spacer(1, h*cm)

def table_style_base(header_rows=1, stripe=True):
    cmds = [
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), HEADER_BG),
        ("TEXTCOLOR",  (0, 0), (-1, header_rows - 1), WHITE),
        ("FONTNAME",   (0, 0), (-1, header_rows - 1), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, header_rows - 1), 8),
        ("ALIGN",      (0, 0), (-1, header_rows - 1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",   (0, header_rows), (-1, -1), "Helvetica"),
        ("FONTSIZE",   (0, header_rows), (-1, -1), 8),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1),
         [WHITE, colors.HexColor("#F8FAFC")] if stripe else [WHITE]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LINEBELOW",    (0, 0), (-1, 0), 1.2, NAVY),
    ]
    return TableStyle(cmds)

def kpi_table(items):
    """items = list of (label, value, bg_color, text_color)"""
    row = []
    for label, value, bg, tc in items:
        inner = Table(
            [[Paragraph(label, S("kL", fontName="Helvetica", fontSize=7.5,
                                 textColor=GRAY_TXT, alignment=TA_CENTER))],
             [Paragraph(value, S("kV", fontName="Helvetica-Bold", fontSize=22,
                                 textColor=tc, alignment=TA_CENTER))]],
            colWidths=[4.0 * cm])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ]))
        row.append(inner)
    t = Table([row], colWidths=[4.3 * cm] * len(items))
    t.setStyle(TableStyle([
        ("ALIGN",  (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

# ─── PAGE TEMPLATE ───────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm

def header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 1.3*cm, PAGE_W, 1.3*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(MARGIN, PAGE_H - 0.85*cm, "FutbolZone — Informe de Ejecucion de Pruebas")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.85*cm,
                           f"ISO/IEC/IEEE 29119-3:2021 | Version {VERSION} | {FECHA_INFORME}")
    # Footer
    canvas.setStrokeColor(GRAY_MID)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.6*cm, PAGE_W - MARGIN, 1.6*cm)
    canvas.setFillColor(GRAY_TXT)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN, 0.9*cm, "SENA — ADSO | Nicolas Felipe Paz Ortiz")
    canvas.drawRightString(PAGE_W - MARGIN, 0.9*cm, f"Pagina {doc.page}")
    canvas.restoreState()

def first_page(canvas, doc):
    canvas.saveState()
    # Gradient-style cover background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#0E2347"))
    canvas.rect(0, 0, PAGE_W, PAGE_H * 0.38, fill=1, stroke=0)
    # Accent line
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H * 0.38, PAGE_W, 0.35*cm, fill=1, stroke=0)
    canvas.restoreState()

def later_pages(canvas, doc):
    header_footer(canvas, doc)

# ─── CONTENT BUILDER ────────────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════════════════════
# 0. PORTADA
# ═══════════════════════════════════════════════════════════════════════════
story.append(SP(5.5))
story.append(P("⚽ FutbolZone", cover_title))
story.append(SP(0.4))
story.append(P("INFORME DE EJECUCIÓN DE PRUEBAS", cover_title))
story.append(SP(0.6))
story.append(P("Norma ISO/IEC/IEEE 29119-3:2021 — Test Execution Report", cover_sub))
story.append(SP(2.5))

meta_rows = [
    ["Versión del documento:", VERSION],
    ["Fecha de elaboración:", FECHA_INFORME],
    ["Proyecto evaluado:", "FutbolZone — Gestión y Reserva de Canchas Sintéticas"],
    ["Programa de formación:", "Análisis y Desarrollo de Software (ADSO)"],
    ["Centro de formación:", "SENA"],
    ["Elaborado por:", "Nicolas Felipe Paz Ortiz"],
    ["Rol:", "Aprendiz ADSO — QA Tester"],
    ["Estado del informe:", "LIMITADO — Ejecución TDD Parcial (Ciclo 1)"],
]
meta_t = Table(meta_rows, colWidths=[6.5*cm, 10.5*cm])
meta_t.setStyle(TableStyle([
    ("FONTNAME",   (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME",   (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE",   (0, 0), (-1, -1), 10),
    ("TEXTCOLOR",  (0, 0), (-1, -1), colors.HexColor("#CBD5E1")),
    ("TEXTCOLOR",  (1, 7), (1, 7), colors.HexColor("#FBBF24")),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING",(0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LINEABOVE",  (0, 0), (-1, 0), 0.4, colors.HexColor("#334155")),
    ("LINEBELOW",  (0, -1),(-1,-1), 0.4, colors.HexColor("#334155")),
]))
story.append(meta_t)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════
# 1. TABLA DE CONTENIDO
# ═══════════════════════════════════════════════════════════════════════════
story.append(P("TABLA DE CONTENIDO", h1))
story.append(hr(NAVY, 1.5))
story.append(SP(0.3))

toc_items = [
    ("1.", "Identificación del Informe", False),
    ("2.", "Introducción", False),
    ("3.", "Objetivo del Informe", False),
    ("4.", "Alcance de la Ejecución", False),
    ("5.", "Documentos de Referencia", False),
    ("6.", "Entorno de Pruebas", False),
    ("7.", "Herramientas Utilizadas", False),
    ("8.", "Resumen de Actividades Ejecutadas", False),
    ("9.", "Resultados Generales — Análisis Estadístico", False),
    ("10.", "Resultados por Módulo", False),
    ("11.", "Análisis de Casos Aprobados (Pasa)", False),
    ("12.", "Análisis de Casos Fallidos (Falla)", False),
    ("13.", "Casos Pendientes o No Ejecutados", False),
    ("14.", "Defectos e Incidencias Identificadas", False),
    ("15.", "Evidencias de Ejecución", False),
    ("16.", "Análisis de Cumplimiento de Criterios de Salida", False),
    ("17.", "Riesgos y Limitaciones Encontradas", False),
    ("18.", "Conclusiones", False),
    ("19.", "Recomendaciones", False),
    ("20.", "Anexos", False),
]
for num, title, sub in toc_items:
    st = toc_sub if sub else toc_style
    story.append(P(f"<b>{num}</b>  {title}", st))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════
# SECCIONES DEL INFORME
# ═══════════════════════════════════════════════════════════════════════════

# ─── 1. IDENTIFICACIÓN ───────────────────────────────────────────────────
story.append(P("1. IDENTIFICACIÓN DEL INFORME", h1))
story.append(hr(NAVY, 1.5))
id_rows = [
    ["Campo", "Detalle"],
    ["Título del documento", "Informe de Ejecución de Pruebas — FutbolZone"],
    ["Código", "IEP-FZ-2026-01"],
    ["Versión", VERSION],
    ["Fecha de elaboración", FECHA_INFORME],
    ["Estado", "LIMITADO — Ejecución TDD Parcial (Ciclo 1 de Pruebas)"],
    ["Proyecto", "FutbolZone — Plataforma Web de Gestión y Reserva de Canchas Sintéticas"],
    ["Programa", "Análisis y Desarrollo de Software (ADSO) — SENA"],
    ["Elaborado por", "Nicolas Felipe Paz Ortiz — Aprendiz ADSO / QA Tester"],
    ["Documento de referencia principal", "Plan de Pruebas FutbolZone v1.0 (Plan_de_Pruebas_FutbolZone.pdf)"],
    ["Matriz de casos de prueba", "matriz-casos-de-prueba-futzone.xlsx (actualizada con columnas de ejecución)"],
    ["Norma aplicada", "ISO/IEC/IEEE 29119-3:2021 — Apartado 7.5 (Test Execution Report)"],
]
id_t = Table(id_rows, colWidths=[5.5*cm, 11.5*cm])
id_t.setStyle(table_style_base())
id_t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
    ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",   (0, 0), (-1, -1), 9),
    ("FONTNAME",   (0, 1), (0, -1), "Helvetica-Bold"),
    ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GRAY_LT]),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING",(0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LINEBELOW",  (0, 0), (-1, 0), 1.2, NAVY),
    ("BACKGROUND", (0, 5), (-1, 5), colors.HexColor("#FEF3C7")),
    ("TEXTCOLOR",  (1, 5), (1, 5), AMBER),
    ("FONTNAME",   (1, 5), (1, 5), "Helvetica-Bold"),
]))
story.append(id_t)
story.append(SP(0.4))
story.append(P("<b>⚠ Nota de clasificación del estado:</b> Este informe se clasifica como LIMITADO porque la "
               "ejecución formal de los 78 casos de prueba diseñados no fue realizada en su totalidad. Los "
               "únicos resultados verificables pertenecen a pruebas unitarias automatizadas (TDD) del módulo "
               "de autenticación. Los 56 casos restantes quedan como Pendientes de Ejecución y los 10 casos "
               "de funcionalidades futuras como No Aplicables.", note_style))

# ─── 2. INTRODUCCIÓN ─────────────────────────────────────────────────────
story.append(P("2. INTRODUCCIÓN", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "El presente Informe de Ejecución de Pruebas documenta el estado real del proceso de verificación "
    "y validación del sistema <b>FutbolZone</b>, una plataforma web orientada a la gestión integral y "
    "reserva de canchas sintéticas de fútbol 5, fútbol 7 y fútbol 11. El proyecto fue desarrollado como "
    "entregable final del programa de formación <b>Análisis y Desarrollo de Software (ADSO)</b> del SENA, "
    "utilizando FastAPI (Python) en el backend, React con TypeScript en el frontend, SQLAlchemy como ORM "
    "y SQLite como motor de base de datos."
))
story.append(P(
    "El ciclo de aseguramiento de calidad contempló tres artefactos principales en secuencia: "
    "(1) el <i>Plan de Pruebas</i> aprobado que define alcance, estrategia, criterios y riesgos; "
    "(2) la <i>Matriz de Casos de Prueba</i> con 78 casos diseñados bajo la norma ISO/IEC/IEEE 29119-3:2021; "
    "y (3) el presente <i>Informe de Ejecución</i>. Este último documenta los resultados obtenidos de "
    "manera fiel: no se inventan resultados, ni se marcan como aprobados casos cuya ejecución no fue registrada."
))
story.append(P(
    "Durante el análisis previo a la elaboración del informe se verificó que la matriz de casos de prueba "
    "<b>no contenía resultados de ejecución diligenciados por el equipo</b> para los 78 casos funcionales "
    "diseñados. Sin embargo, el repositorio contiene una suite de <b>16 pruebas unitarias automatizadas</b> "
    "(actividad_tdd/test_auth.py y actividad_tdd/test_ui.py) que fueron ejecutadas y validadas durante "
    "la elaboración de este informe, obteniendo resultado <b>16/16 OK</b>. Estos constituyen los únicos "
    "resultados formalmente registrables en el presente ciclo."
))

# ─── 3. OBJETIVO ─────────────────────────────────────────────────────────
story.append(P("3. OBJETIVO DEL INFORME", h1))
story.append(hr(NAVY, 1.5))
story.append(P("<b>Objetivo general:</b> Documentar de forma objetiva, trazable y alineada con la norma "
               "ISO/IEC/IEEE 29119-3:2021 el estado real de la ejecución de las pruebas diseñadas para "
               "el sistema FutbolZone, identificando los resultados verificables, las limitaciones del "
               "ciclo actual y las acciones requeridas para completar la cobertura de pruebas."))
story.append(P("<b>Objetivos específicos:</b>"))
for obj in [
    "Contrastar los 78 casos de prueba diseñados con los resultados de ejecución disponibles.",
    "Registrar los 12 casos aprobados mediante pruebas unitarias TDD automatizadas (16 aserciones).",
    "Identificar los 56 casos pendientes de ejecución manual contra el sistema real (FastAPI + React).",
    "Identificar los 10 casos No Aplicables correspondientes a funcionalidades del Roadmap Futuro.",
    "Documentar el hallazgo técnico identificado en el controlador de registro de usuarios (HTTP 200 en error).",
    "Contrastar los resultados con los criterios de salida definidos en el Plan de Pruebas.",
    "Formular recomendaciones concretas para completar el ciclo de ejecución en un Sprint siguiente.",
]:
    story.append(P(f"• {obj}", body_bullet))

# ─── 4. ALCANCE ──────────────────────────────────────────────────────────
story.append(P("4. ALCANCE DE LA EJECUCIÓN", h1))
story.append(hr(NAVY, 1.5))
story.append(P("<b>Dentro del alcance ejecutado en el Ciclo 1:</b>"))
for item in [
    "16 pruebas unitarias TDD del módulo de Autenticación (actividad_tdd): registro, login, validación de email, fortaleza de contraseña, bloqueo por intentos fallidos, recuperación de contraseña mediante tokens, e interfaz de consola (CLI mock).",
    "Verificación del estado de la base de datos SQLite (futbolzone.db): 5 usuarios, 3 canchas, 8 reservas confirmadas.",
    "Revisión estática del código fuente: 10 modelos SQLAlchemy, 34 endpoints FastAPI, 12 componentes React relevantes.",
]:
    story.append(P(f"• {item}", body_bullet))

story.append(SP(0.2))
story.append(P("<b>Fuera del alcance de este ciclo (Pendiente — Ciclo 2):</b>"))
for item in [
    "56 casos de prueba que requieren ejecución manual contra el sistema completo (backend FastAPI corriendo + frontend React activo + herramienta Postman/Bruno o navegador web).",
    "Pruebas de integración frontend-backend: flujos completos desde la interfaz React hasta la API REST.",
    "Pruebas de rendimiento, carga y seguridad (penetración) definidas en el Plan de Pruebas.",
    "10 casos de funcionalidades no implementadas (Roadmap Futuro: HU-16 a HU-20, HU-35 a HU-38).",
]:
    story.append(P(f"• {item}", body_bullet))

# ─── 5. DOCUMENTOS DE REFERENCIA ─────────────────────────────────────────
story.append(P("5. DOCUMENTOS DE REFERENCIA", h1))
story.append(hr(NAVY, 1.5))
ref_rows = [
    ["#", "Documento", "Uso en el informe"],
    ["1", "ISO/IEC/IEEE 29119-3:2021", "Norma de estructura del informe (Apartado 7.5 Test Execution Report)"],
    ["2", "Plan_de_Pruebas_FutbolZone.pdf", "Criterios de entrada/salida, alcance aprobado, riesgos y estrategia"],
    ["3", "matriz-casos-de-prueba-futzone.xlsx", "78 casos diseñados; actualizada con columnas de ejecución"],
    ["4", "actividad_tdd/INFORME_EVIDENCIA_TDD.md", "Evidencia del proceso TDD ciclo Rojo-Verde-Refactorizar"],
    ["5", "actividad_tdd/test_auth.py", "Suite de 14 pruebas unitarias: registro, login, seguridad"],
    ["6", "actividad_tdd/test_ui.py", "2 pruebas de interfaz CLI con unittest.mock"],
    ["7", "actividad_tdd/auth.py", "Implementación del módulo UserManager bajo TDD"],
    ["8", "backend/app/controllers/", "Lógica real del backend FastAPI (revisión estática)"],
    ["9", "backend/futbolzone.db", "Base de datos SQLite real del proyecto (consultada directamente)"],
    ["10", "Backlog_FutbolZone_Navegable.xlsx", "Historias de usuario HU-01 a HU-38, estados y prioridades"],
]
ref_t = Table(ref_rows, colWidths=[0.8*cm, 6.0*cm, 10.2*cm])
ref_t.setStyle(table_style_base())
story.append(ref_t)

# ─── 6. ENTORNO DE PRUEBAS ───────────────────────────────────────────────
story.append(P("6. ENTORNO DE PRUEBAS", h1))
story.append(hr(NAVY, 1.5))
story.append(P("<b>6.1 Entorno donde se realizaron las pruebas TDD ejecutadas:</b>"))
env_rows = [
    ["Componente", "Especificación verificada"],
    ["Sistema operativo", "Windows 11 (plataforma de desarrollo y ejecución)"],
    ["Intérprete Python", "CPython 3.14 (confirmado por .pyc en __pycache__)"],
    ["Framework de pruebas", "unittest (módulo estándar de Python 3.x) + unittest.mock"],
    ["Módulos bajo prueba", "actividad_tdd/auth.py (UserManager) | actividad_tdd/ui.py (AuthUI)"],
    ["Base de datos en pruebas", "No aplica para TDD (UserManager usa dict en memoria)"],
    ["IDE/Editor", "Visual Studio Code (referenciado en INFORME_EVIDENCIA_TDD.md)"],
    ["Tiempo de ejecución suite TDD", "0.001 segundos (16 tests — sin dependencias externas)"],
]
env_t = Table(env_rows, colWidths=[5.5*cm, 11.5*cm])
env_t.setStyle(table_style_base())
story.append(env_t)
story.append(SP(0.3))
story.append(P("<b>6.2 Entorno requerido para ejecución del Ciclo 2 (Pendiente):</b>"))
env2_rows = [
    ["Componente", "Requerimiento"],
    ["Backend API", "FastAPI en http://localhost:5000 (python main.py en /backend)"],
    ["Frontend", "React + Vite en http://localhost:5173 (pnpm run dev en /frontend)"],
    ["Base de datos", "SQLite — backend/futbolzone.db (inicializada con datos semilla)"],
    ["Cliente REST", "Postman, Bruno, Insomnia o curl para pruebas de API directas"],
    ["Navegador", "Google Chrome / Firefox (pruebas de interfaz web)"],
    ["Estado DB requerido", "5 usuarios activos | 3 canchas activas | admin@futbolzone.com disponible"],
]
env2_t = Table(env2_rows, colWidths=[5.5*cm, 11.5*cm])
env2_t.setStyle(table_style_base())
story.append(env2_t)

# ─── 7. HERRAMIENTAS ─────────────────────────────────────────────────────
story.append(P("7. HERRAMIENTAS UTILIZADAS", h1))
story.append(hr(NAVY, 1.5))
tools_rows = [
    ["Herramienta", "Versión", "Propósito", "Ciclo"],
    ["Python unittest", "Estándar 3.14", "Ejecución de pruebas TDD automatizadas", "Ciclo 1 ✓"],
    ["unittest.mock", "Estándar 3.14", "Simulación de input/print en pruebas de UI CLI", "Ciclo 1 ✓"],
    ["openpyxl", "Instalada", "Generación y actualización de la matriz de casos de prueba (.xlsx)", "Ciclo 1 ✓"],
    ["ReportLab 5.1.0", "5.1.0", "Generación del presente informe en formato PDF", "Ciclo 1 ✓"],
    ["SQLite (nativo)", "3.x", "Consulta directa de la base de datos futbolzone.db", "Ciclo 1 ✓"],
    ["SQLAlchemy (ORM)", "Instalada", "Acceso programático a modelos para inspección del estado", "Ciclo 1 ✓"],
    ["Postman / Bruno", "N/D", "Pruebas de API REST (FastAPI endpoints)", "Ciclo 2 — Pendiente"],
    ["Navegador web", "N/D", "Pruebas de interfaz React (UI/UX, flujos de usuario)", "Ciclo 2 — Pendiente"],
    ["pytest + httpx", "N/D", "Pruebas de integración FastAPI con cliente de prueba", "Ciclo 2 — Pendiente"],
]
tools_t = Table(tools_rows, colWidths=[4.5*cm, 2.5*cm, 7.5*cm, 2.5*cm])
tools_t.setStyle(table_style_base())
story.append(tools_t)

# ─── 8. RESUMEN DE ACTIVIDADES ───────────────────────────────────────────
story.append(P("8. RESUMEN DE ACTIVIDADES EJECUTADAS", h1))
story.append(hr(NAVY, 1.5))
act_rows = [
    ["#", "Actividad realizada", "Resultado", "Evidencia disponible"],
    ["1", "Verificación del estado de la matriz de casos de prueba", "Sin resultados de ejecución diligenciados por el equipo", "matriz-casos-de-prueba-futzone.xlsx (revisión directa)"],
    ["2", "Ejecución de suite TDD — TestUserRegistration (6 tests)", "6/6 OK — 0 fallos", "Terminal: Ran 6 tests in 0.001s — OK"],
    ["3", "Ejecución de suite TDD — TestUserLogin (3 tests)", "3/3 OK — 0 fallos", "Terminal: Ran 3 tests in 0.001s — OK"],
    ["4", "Ejecución de suite TDD — TestSecurityFeatures (5 tests)", "5/5 OK — 0 fallos", "Terminal: Ran 5 tests in 0.001s — OK"],
    ["5", "Ejecución de suite TDD — TestAuthUI (2 tests)", "2/2 OK — 0 fallos", "Terminal: Ran 2 tests in 0.001s — OK"],
    ["6", "Consulta directa de base de datos futbolzone.db", "5 usuarios | 3 canchas | 8 reservas verificadas", "SQLAlchemy SessionLocal() query"],
    ["7", "Revisión estática de controladores FastAPI", "Hallazgo: HTTP 200 en error de duplicado de email (registro)", "backend/app/controllers/usuario_controller.py L68"],
    ["8", "Actualización de la matriz con columnas de ejecución (G, H, I)", "78 filas actualizadas: 12 Pasa | 56 No ejecutado | 10 No aplicable", "matriz-casos-de-prueba-futzone.xlsx actualizada"],
]
act_t = Table(act_rows, colWidths=[0.7*cm, 5.8*cm, 4.5*cm, 6.0*cm])
act_t.setStyle(table_style_base())
story.append(act_t)

# ─── 9. RESULTADOS GENERALES ─────────────────────────────────────────────
story.append(PageBreak())
story.append(P("9. RESULTADOS GENERALES — ANÁLISIS ESTADÍSTICO", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "Las cifras presentadas a continuación se calcularon exclusivamente a partir de los resultados "
    "registrados en la columna <i>Estado</i> de la matriz de casos de prueba actualizada "
    "(matriz-casos-de-prueba-futzone.xlsx). No se imputan resultados supuestos.",
    note_style))
story.append(SP(0.3))

story.append(kpi_table([
    ("TOTAL CASOS\nDISEÑADOS", "78", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF")),
    ("EJECUTADOS\n(TDD)", "12", PASS_BG, PASS_G),
    ("NO EJECUTADOS\n(MANUAL PEND.)", "56", NOEX_BG, GRAY_TXT),
    ("NO APLICABLES\n(ROADMAP)", "10", NOAP_BG, AMBER),
]))
story.append(SP(0.4))
story.append(kpi_table([
    ("PASA", "12", PASS_BG, PASS_G),
    ("FALLA", "0", colors.HexColor("#FFF"), FAIL_R),
    ("% EJECUCIÓN\n(12/78)", "15.4%", colors.HexColor("#EFF6FF"), colors.HexColor("#1E40AF")),
    ("% APROBACIÓN\n(12/12 ejec.)", "100%", PASS_BG, PASS_G),
]))
story.append(SP(0.4))
story.append(P(
    "<b>Fórmulas aplicadas (ISO/IEC/IEEE 29119-3):</b>",
    bold_body))
formulas = [
    ("Porcentaje de ejecución", "Casos ejecutados / Total diseñados × 100", "12 / 78 × 100 = 15.4%"),
    ("Porcentaje de aprobación", "Casos Pasa / Casos ejecutados × 100", "12 / 12 × 100 = 100.0%"),
    ("Porcentaje de fallos", "Casos Falla / Casos ejecutados × 100", "0 / 12 × 100 = 0.0%"),
]
form_t = Table(
    [["Indicador", "Fórmula", "Resultado"]] + [[a, b, c] for a, b, c in formulas],
    colWidths=[5.0*cm, 8.0*cm, 4.0*cm])
form_t.setStyle(table_style_base())
story.append(form_t)
story.append(SP(0.3))
story.append(P(
    "<b>Interpretación:</b> El porcentaje de ejecución del 15.4% refleja que solo los casos cubiertos "
    "por las pruebas unitarias TDD del módulo de autenticación fueron ejecutados formalmente en este ciclo. "
    "El 100% de aprobación sobre los casos ejecutados indica que todos los escenarios TDD pasaron sin "
    "fallos. <b>Este dato no debe interpretarse como un indicador de calidad global del sistema</b>, dado "
    "que el 71.8% de los casos (56 casos funcionales de la aplicación real) permanecen sin ejecutar.",
    note_style))

# ─── 10. RESULTADOS POR MÓDULO ───────────────────────────────────────────
story.append(P("10. RESULTADOS POR MÓDULO", h1))
story.append(hr(NAVY, 1.5))

mod_rows = [
    ["Módulo", "Casos\nDiseñados", "Pasa", "Falla", "No Ejec.", "No Aplic.", "% Ejec.", "Estado"],
    ["Autenticación",   "4",  "4",  "0", "0",  "0",  "100%", "EJECUTADO"],
    ["Seguridad",       "16", "8",  "0", "8",  "0",  "50%",  "PARCIAL"],
    ["Reservas",        "17", "0",  "0", "17", "0",  "0%",   "PENDIENTE"],
    ["Canchas",         "11", "0",  "0", "11", "0",  "0%",   "PENDIENTE"],
    ["Agendamiento",    "4",  "0",  "0", "4",  "0",  "0%",   "PENDIENTE"],
    ["Administración",  "2",  "0",  "0", "2",  "0",  "0%",   "PENDIENTE"],
    ["Reportes",        "3",  "0",  "0", "3",  "0",  "0%",   "PENDIENTE"],
    ["Personal",        "4",  "0",  "0", "4",  "0",  "0%",   "PENDIENTE"],
    ["UI / UX",         "4",  "0",  "0", "3",  "0",  "25%",  "PARCIAL (1 TDD)"],
    ["Torneos",         "6",  "0",  "0", "3",  "3",  "0%",   "PARCIAL IMPL."],
    ["Pagos",           "2",  "0",  "0", "0",  "2",  "N/A",  "NO APLICABLE"],
    ["Comprobantes",    "1",  "0",  "0", "0",  "1",  "N/A",  "NO APLICABLE"],
    ["Notificaciones",  "1",  "0",  "0", "0",  "1",  "N/A",  "NO APLICABLE"],
    ["Fidelización",    "1",  "0",  "0", "0",  "1",  "N/A",  "NO APLICABLE"],
    ["Integraciones",   "1",  "0",  "0", "0",  "1",  "N/A",  "NO APLICABLE"],
    ["DevOps",          "1",  "0",  "0", "0",  "1",  "N/A",  "NO APLICABLE"],
    ["TOTAL",          "78", "12",  "0","56", "10",  "15.4%","—"],
]

col_widths_mod = [4.0*cm, 1.6*cm, 1.2*cm, 1.2*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3.5*cm]
mod_t = Table(mod_rows, colWidths=col_widths_mod, repeatRows=1)
mod_style = table_style_base()
# Color last row
n_mod = len(mod_rows)
mod_style.add("BACKGROUND", (0, n_mod-1), (-1, n_mod-1), SUBHDR_BG)
mod_style.add("FONTNAME",   (0, n_mod-1), (-1, n_mod-1), "Helvetica-Bold")
mod_style.add("ALIGN", (1,1), (-2,-1), "CENTER")
# Color "EJECUTADO" cells
for i, row in enumerate(mod_rows[1:], 1):
    st = row[7]
    if st == "EJECUTADO":
        mod_style.add("BACKGROUND", (7, i), (7, i), PASS_BG)
        mod_style.add("TEXTCOLOR",  (7, i), (7, i), PASS_G)
        mod_style.add("FONTNAME",   (7, i), (7, i), "Helvetica-Bold")
    elif "PARCIAL" in st:
        mod_style.add("BACKGROUND", (7, i), (7, i), NOAP_BG)
        mod_style.add("TEXTCOLOR",  (7, i), (7, i), AMBER)
        mod_style.add("FONTNAME",   (7, i), (7, i), "Helvetica-Bold")
    elif st == "PENDIENTE":
        mod_style.add("TEXTCOLOR",  (7, i), (7, i), GRAY_TXT)
    elif "NO APLICABLE" in st:
        mod_style.add("TEXTCOLOR",  (7, i), (7, i), AMBER)
mod_t.setStyle(mod_style)
story.append(mod_t)

# ─── 11. ANÁLISIS CASOS APROBADOS ────────────────────────────────────────
story.append(P("11. ANÁLISIS DE CASOS APROBADOS (PASA)", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "Se registraron <b>12 casos con estado Pasa</b>, todos verificados mediante las suites de pruebas "
    "unitarias automatizadas (TDD) del directorio <code>actividad_tdd/</code>. "
    "El resultado de la ejecución fue <b>Ran 16 tests in 0.001s — OK</b> (el diferencial entre "
    "12 casos de la matriz y 16 aserciones TDD se debe a que algunos casos de prueba son cubiertos "
    "por múltiples aserciones individuales dentro de la suite unittest)."))
story.append(SP(0.2))

pass_rows = [
    ["ID Caso", "Historia", "Módulo", "Escenario TDD que lo cubre", "Resultado"],
    ["CP-HU01-001", "HU-01", "Autenticación", "test_register_user_success", "PASA"],
    ["CP-HU01-002", "HU-01", "Autenticación", "test_register_invalid_email_fails", "PASA"],
    ["CP-HU01-003", "HU-01", "Autenticación", "test_register_short_password_fails\ntest_register_password_without_number_fails\ntest_register_password_without_uppercase_fails", "PASA"],
    ["CP-HU01-004", "HU-01", "Autenticación", "test_register_duplicate_email_fails", "PASA"],
    ["CP-HU02-001", "HU-02", "Seguridad", "test_login_success", "PASA"],
    ["CP-HU02-002", "HU-02", "Seguridad", "test_login_wrong_password_fails", "PASA"],
    ["CP-HU02-003", "HU-02", "Seguridad", "test_login_nonexistent_user_fails", "PASA"],
    ["CP-HU02-004", "HU-02", "UI / UX (CLI)", "test_ui_login_successful_flow", "PASA"],
    ["CP-HU03-001", "HU-03", "Seguridad", "test_generate_reset_token_success\ntest_reset_password_with_valid_token", "PASA"],
    ["CP-HU03-002", "HU-03", "Seguridad", "test_reset_password_with_invalid_token_fails", "PASA"],
    ["CP-HU03-003", "HU-03", "Seguridad", "test_account_locks_after_three_failed_logins\ntest_successful_login_resets_failed_attempts", "PASA"],
    ["CP-HU13-001", "HU-13", "UI / UX (CLI)", "test_ui_register_flow", "PASA"],
]
pass_t = Table(pass_rows, colWidths=[2.5*cm, 1.5*cm, 2.2*cm, 7.3*cm, 1.5*cm], repeatRows=1)
ps = table_style_base()
for i in range(1, len(pass_rows)):
    ps.add("BACKGROUND", (4, i), (4, i), PASS_BG)
    ps.add("TEXTCOLOR",  (4, i), (4, i), PASS_G)
    ps.add("FONTNAME",   (4, i), (4, i), "Helvetica-Bold")
    ps.add("ALIGN",      (4, i), (4, i), "CENTER")
pass_t.setStyle(ps)
story.append(pass_t)
story.append(SP(0.2))
story.append(P(
    "<b>Aclaración importante:</b> Los 12 casos aprobados pertenecen exclusivamente al módulo de "
    "autenticación de la capa de lógica de negocio (actividad_tdd/auth.py). "
    "No verifican el comportamiento completo del endpoint FastAPI /api/usuarios/, ni la integración "
    "con SQLite, ni la emisión real de tokens JWT, ni la interfaz React. "
    "Su valor es validar la lógica de dominio en aislamiento, siguiendo el ciclo TDD.",
    note_style))

# ─── 12. ANÁLISIS CASOS FALLIDOS ─────────────────────────────────────────
story.append(P("12. ANÁLISIS DE CASOS FALLIDOS (FALLA)", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "No se registraron casos con estado <b>Falla</b> en el presente ciclo de ejecución. "
    "Las 16 pruebas unitarias TDD ejecutadas resultaron en <b>0 fallos</b>. "
    "No obstante, durante la revisión estática del código fuente se identificó "
    "<b>un hallazgo técnico relevante</b> que debe documentarse como defecto potencial, "
    "dado que podría generar un caso fallido al ejecutar el caso CP-HU01-004 "
    "contra el endpoint real de la API FastAPI."))

# ─── 13. CASOS PENDIENTES ─────────────────────────────────────────────────
story.append(P("13. CASOS PENDIENTES O NO EJECUTADOS", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "Se registran <b>66 casos sin resultado de ejecución</b> en el presente ciclo, "
    "distribuidos en dos categorías:"))
pend_rows = [
    ["Categoría", "Cantidad", "Causa", "Módulos afectados"],
    ["No ejecutado\n(Pendiente de ejecución manual)", "56",
     "El entorno de ejecución (backend FastAPI + BD + frontend React) no fue iniciado durante este ciclo. No se registraron resultados manuales en la matriz.",
     "Reservas, Canchas, Agendamiento, Administración, Reportes, Personal, Torneos (parcial), UI/UX (parcial)"],
    ["No aplicable\n(Funcionalidad no implementada)", "10",
     "Las historias de usuario correspondientes (HU-16 a HU-20, HU-35 a HU-38) no tienen código en backend ni frontend. No es posible ejecutar pruebas sin la funcionalidad.",
     "Pagos, Comprobantes QR, Notificaciones, Fidelización, Google Calendar, Brackets, Lector QR, CI/CD, Auditoría"],
]
pend_t = Table(pend_rows, colWidths=[3.5*cm, 1.5*cm, 6.5*cm, 5.5*cm])
pt = table_style_base()
pt.add("BACKGROUND", (0, 2), (-1, 2), NOAP_BG)
pend_t.setStyle(pt)
story.append(pend_t)
story.append(SP(0.2))
story.append(P(
    "Para completar la ejecución de los 56 casos pendientes se requiere: iniciar el servidor backend "
    "(cd backend && uvicorn main:app --reload --port 5000), iniciar el frontend "
    "(cd frontend && pnpm run dev), y contar con una herramienta de pruebas REST (Postman, Bruno) "
    "y un navegador web configurado. Los casos deben ejecutarse en el orden definido por las "
    "dependencias de datos: primero HU-01 (registro), luego HU-02 (login/token), y así sucesivamente.",
    note_style))

# ─── 14. DEFECTOS E INCIDENCIAS ───────────────────────────────────────────
story.append(PageBreak())
story.append(P("14. DEFECTOS E INCIDENCIAS IDENTIFICADAS", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "Se identificó <b>1 hallazgo técnico</b> mediante revisión estática del código fuente. "
    "No se registraron fallos en las pruebas unitarias ejecutadas. "
    "El hallazgo no implica una prueba fallida ejecutada, sino una <b>observación de diseño de API</b> "
    "que podría generar un caso fallido al ejecutar CP-HU01-004 contra el endpoint real."))
story.append(SP(0.2))

defect_rows = [
    ["Campo", "Detalle"],
    ["ID del hallazgo", "HLZ-001"],
    ["ID del caso relacionado", "CP-HU01-004"],
    ["Historia de usuario", "HU-01 — Registro de Cuenta de Cliente"],
    ["Módulo afectado", "Autenticación — Registro de Usuarios"],
    ["Archivo fuente", "backend/app/controllers/usuario_controller.py — Línea 68"],
    ["Comportamiento esperado (caso)",
     "HTTP 400 Bad Request o HTTP 409 Conflict cuando se intenta registrar un correo ya existente en la BD."],
    ["Comportamiento observado (código)",
     "El controlador retorna api_response(False, 'El correo ya está registrado', error='Duplicate email') "
     "sin cambiar el código HTTP. FastAPI envuelve esta respuesta en HTTP 200 OK, lo que contradice "
     "las convenciones REST (un 200 no debe indicar fallo)."],
    ["Descripción técnica",
     "La función api_response() (backend/app/utils/response.py) no establece el código de estado HTTP. "
     "FastAPI utiliza 200 por defecto. El resultado esperado en el caso CP-HU01-004 especifica "
     "HTTP 400 o 409, por lo que al ejecutar el caso contra el endpoint real, el resultado "
     "obtenido sería HTTP 200, generando un estado Falla."],
    ["Evidencia", "Revisión estática de backend/app/controllers/usuario_controller.py L65-68"],
    ["Impacto funcional",
     "Bajo (la validación lógica es correcta — no se crea el duplicado). "
     "Medio desde perspectiva de integración — clientes REST y frontend deben verificar "
     "el campo 'success' en el body además del código HTTP para detectar el error."],
    ["Recomendación",
     "Cambiar la respuesta en el controlador para usar HTTPException(status_code=400) o "
     "establecer status_code=409 en la respuesta cuando el correo ya existe. "
     "Esto alinea la API con el estándar REST y hace que el caso CP-HU01-004 pase correctamente."],
    ["Estado del hallazgo", "Abierto — Pendiente de corrección y re-prueba"],
    ["Prioridad sugerida", "Media (no bloquea funcionalidad, pero viola convención REST)"],
]
def_t = Table(defect_rows, colWidths=[4.5*cm, 12.5*cm])
ds = table_style_base()
ds.add("BACKGROUND", (0, 7), (-1, 7), colors.HexColor("#FEF9C3"))
ds.add("BACKGROUND", (0, 8), (-1, 8), colors.HexColor("#FEF9C3"))
ds.add("BACKGROUND", (0, -2), (-1, -2), NOAP_BG)
ds.add("BACKGROUND", (0, -1), (-1, -1), NOAP_BG)
def_t.setStyle(ds)
story.append(def_t)

# ─── 15. EVIDENCIAS ───────────────────────────────────────────────────────
story.append(P("15. EVIDENCIAS DE EJECUCIÓN", h1))
story.append(hr(NAVY, 1.5))
story.append(P("<b>15.1 Evidencia verificable: Ejecución suite TDD automatizada</b>"))
story.append(P(
    "El siguiente registro de consola fue obtenido al ejecutar el comando "
    "<code>python -m unittest discover actividad_tdd -v</code> durante la elaboración de este informe:"))
story.append(SP(0.1))

console_data = """test_account_locks_after_three_failed_logins (test_auth.TestSecurityFeatures...) ... ok
test_generate_reset_token_success (test_auth.TestSecurityFeatures...) ... ok
test_reset_password_with_invalid_token_fails (test_auth.TestSecurityFeatures...) ... ok
test_reset_password_with_valid_token (test_auth.TestSecurityFeatures...) ... ok
test_successful_login_resets_failed_attempts (test_auth.TestSecurityFeatures...) ... ok
test_login_nonexistent_user_fails (test_auth.TestUserLogin...) ... ok
test_login_success (test_auth.TestUserLogin...) ... ok
test_login_wrong_password_fails (test_auth.TestUserLogin...) ... ok
test_register_duplicate_email_fails (test_auth.TestUserRegistration...) ... ok
test_register_invalid_email_fails (test_auth.TestUserRegistration...) ... ok
test_register_password_without_number_fails (test_auth.TestUserRegistration...) ... ok
test_register_password_without_uppercase_fails (test_auth.TestUserRegistration...) ... ok
test_register_short_password_fails (test_auth.TestUserRegistration...) ... ok
test_register_user_success (test_auth.TestUserRegistration...) ... ok
test_ui_login_successful_flow (test_ui.TestAuthUI...) ... ok
test_ui_register_flow (test_ui.TestAuthUI...) ... ok
----------------------------------------------------------------------
Ran 16 tests in 0.001s
OK"""

console_t = Table([[console_data]], colWidths=[17.0*cm])
console_t.setStyle(TableStyle([
    ("FONTNAME",    (0,0), (-1,-1), "Courier"),
    ("FONTSIZE",    (0,0), (-1,-1), 7.5),
    ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#0F172A")),
    ("TEXTCOLOR",   (0,0), (-1,-1), colors.HexColor("#4ADE80")),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
    ("RIGHTPADDING",(0,0), (-1,-1), 10),
    ("TOPPADDING",  (0,0), (-1,-1), 8),
    ("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("BOX",         (0,0), (-1,-1), 1, TEAL),
]))
story.append(console_t)
story.append(SP(0.3))

story.append(P("<b>15.2 Evidencia verificable: Estado de la base de datos SQLite</b>"))
story.append(P("Consulta ejecutada directamente mediante SQLAlchemy (python -c) sobre backend/futbolzone.db:"))
db_rows = [
    ["Tabla", "Registros verificados", "Detalle"],
    ["usuarios", "5 registros",
     "ID=1 admin@futbolzone.com (admin, activo)\nID=2 cliente@futbolzone.com (cliente, activo)\nIDs 3,4,5: clientes registrados, activos"],
    ["canchas", "3 registros",
     "ID=1 Cancha Central (futbol_5, $40.000/h, activa)\nID=2 Cancha Norte (futbol_7, $70.000/h, activa)\nID=3 Cancha Sur (futbol_11, $100.000/h, activa)"],
    ["reservas", "8 registros",
     "5 completadas | 1 confirmada | 2 pendientes\nUltima fecha: 2026-09-05 — sin solapamientos detectados"],
]
db_t = Table(db_rows, colWidths=[2.5*cm, 2.5*cm, 12.0*cm])
db_t.setStyle(table_style_base())
story.append(db_t)
story.append(SP(0.2))
story.append(P("<b>15.3 Evidencias NO disponibles en este ciclo:</b>"))
for ev in [
    "Capturas de pantalla de la interfaz React ejecutándose en el navegador.",
    "Respuestas HTTP capturadas desde Postman, Bruno o curl para los endpoints FastAPI.",
    "Registros de consola del servidor uvicorn durante la ejecución de pruebas.",
    "Resultados de ejecución manual diligenciados por el equipo en la matriz de casos.",
    "Evidencias de pruebas de rendimiento, seguridad de penetración o carga del sistema.",
]:
    story.append(P(f"• {ev}", body_bullet))

# ─── 16. CRITERIOS DE SALIDA ──────────────────────────────────────────────
story.append(P("16. ANÁLISIS DE CUMPLIMIENTO DE CRITERIOS DE SALIDA", h1))
story.append(hr(NAVY, 1.5))
story.append(P(
    "Se contrastan los criterios de salida definidos en el Plan de Pruebas FutbolZone v1.0 "
    "con el estado real del ciclo de ejecución actual:"))
story.append(SP(0.1))
cs_rows = [
    ["Criterio de salida (Plan de Pruebas)", "Estado\nactual", "Observación"],
    ["Ejecución del 100% de los casos de prueba diseñados",
     "NO CUMPLE", "Solo el 15.4% fue ejecutado (12/78 casos vía TDD)"],
    ["Porcentaje de aprobación ≥ 85% sobre casos ejecutados",
     "CUMPLE\n(parcial)", "100% de los 12 casos ejecutados pasan. Base muestral insuficiente."],
    ["0 defectos de severidad Alta sin resolver",
     "CUMPLE\n(parcial)", "El hallazgo HLZ-001 es de impacto Medio. No hay defectos bloqueantes conocidos en las pruebas ejecutadas."],
    ["Cobertura de los 7 módulos críticos del sistema",
     "NO CUMPLE", "Solo el módulo de Autenticación fue ejecutado. Reservas, Canchas, Administración, Reportes, Personal y UI principal: 0% ejecutado."],
    ["Evidencias de ejecución disponibles para todos los casos Pasa",
     "CUMPLE\n(parcial)", "Evidencia disponible para los 12 casos TDD. Ninguna evidencia para los 56 pendientes."],
    ["Revisión y aprobación del informe por el QA Lead",
     "PENDIENTE", "El presente informe está en estado borrador/elaboración. Requiere revisión formal."],
]
cs_t = Table(cs_rows, colWidths=[7.0*cm, 2.5*cm, 7.5*cm])
css = table_style_base()
for i, row in enumerate(cs_rows[1:], 1):
    st = row[1]
    if "NO CUMPLE" in st:
        css.add("BACKGROUND", (1, i), (1, i), FAIL_BG)
        css.add("TEXTCOLOR",  (1, i), (1, i), FAIL_R)
        css.add("FONTNAME",   (1, i), (1, i), "Helvetica-Bold")
    elif "CUMPLE" in st:
        css.add("BACKGROUND", (1, i), (1, i), PASS_BG)
        css.add("TEXTCOLOR",  (1, i), (1, i), PASS_G)
        css.add("FONTNAME",   (1, i), (1, i), "Helvetica-Bold")
    elif "PENDIENTE" in st:
        css.add("BACKGROUND", (1, i), (1, i), NOAP_BG)
        css.add("TEXTCOLOR",  (1, i), (1, i), AMBER)
        css.add("FONTNAME",   (1, i), (1, i), "Helvetica-Bold")
cs_t.setStyle(css)
story.append(cs_t)
story.append(SP(0.2))
story.append(P(
    "<b>Conclusión sobre criterios de salida:</b> El ciclo actual <b>NO cumple</b> los criterios de "
    "salida establecidos en el Plan de Pruebas. Los criterios de ejecución completa y cobertura de "
    "módulos críticos no se satisfacen con el 15.4% de ejecución registrado. "
    "Se recomienda no considerar el sistema como aprobado para paso a producción hasta completar "
    "el Ciclo 2 de ejecución manual.",
    note_style))

# ─── 17. RIESGOS Y LIMITACIONES ──────────────────────────────────────────
story.append(P("17. RIESGOS Y LIMITACIONES ENCONTRADAS", h1))
story.append(hr(NAVY, 1.5))

riesgos_rows = [
    ["#", "Riesgo / Limitación", "Impacto", "Acción recomendada"],
    ["R1", "La matriz de casos de prueba no fue diligenciada con resultados de ejecución manual por el equipo. 56 casos no tienen estado de ejecución.",
     "Alto — Imposibilita el análisis estadístico completo y la validación del sistema funcional.",
     "Programar sesión de ejecución manual (Ciclo 2) con el sistema corriendo en localhost."],
    ["R2", "No se dispone de capturas de pantalla, registros de Postman ni evidencias de ejecución funcional contra la API FastAPI real.",
     "Alto — El informe no puede certificar el comportamiento de los 56 casos funcionales.",
     "Usar Postman/Bruno para ejecutar y exportar colecciones de prueba contra localhost:5000."],
    ["R3", "Hallazgo HLZ-001: el controlador de registro retorna HTTP 200 en caso de email duplicado, en lugar de HTTP 400/409.",
     "Medio — Viola convención REST; puede confundir a clientes API y frontend.",
     "Corregir usuario_controller.py para lanzar HTTPException(status_code=409) en caso de duplicado."],
    ["R4", "Las pruebas TDD del módulo actividad_tdd verifican la lógica en UserManager (dict en memoria), no en el backend FastAPI + SQLite real. Son pruebas de unidad, no de integración.",
     "Medio — La cobertura real del sistema FastAPI es desconocida.",
     "Implementar pruebas de integración con pytest + TestClient de FastAPI sobre la BD de test."],
    ["R5", "El módulo de Torneos tiene backend implementado pero frontend desacoplado (TorneosView.tsx usa localStorage mock). Los 6 casos de Torneos no pueden ejecutarse end-to-end.",
     "Medio — La funcionalidad de torneos está parcialmente disponible.",
     "Conectar TorneosView.tsx a los endpoints /api/torneos/ y ejecutar las pruebas de integración."],
    ["R6", "Las 9 historias del Roadmap Futuro (HU-16 a HU-20, HU-35 a HU-38) no tienen implementación. Los 10 casos asociados están en estado No Aplicable.",
     "Bajo para el ciclo actual — no afecta el MVP.",
     "Mantener como especificación técnica. Incluir en Sprint de desarrollo siguiente."],
    ["R7", "No se ejecutaron pruebas de rendimiento, carga ni seguridad (penetración).",
     "Medio — El sistema no ha sido evaluado bajo condiciones de múltiples usuarios concurrentes.",
     "Incluir pruebas con Locust o k6 en el Ciclo 2 según el Plan de Pruebas aprobado."],
]
risk_t = Table(riesgos_rows, colWidths=[0.7*cm, 6.0*cm, 4.5*cm, 5.8*cm], repeatRows=1)
risk_t.setStyle(table_style_base())
story.append(risk_t)

# ─── 18. CONCLUSIONES ─────────────────────────────────────────────────────
story.append(PageBreak())
story.append(P("18. CONCLUSIONES", h1))
story.append(hr(NAVY, 1.5))

conclusiones = [
    ("1. El ciclo de pruebas Ciclo 1 es parcial e insuficiente para certificar la calidad del sistema.",
     "Solo el 15.4% de los casos diseñados (12/78) fue ejecutado. Los criterios de salida definidos en el "
     "Plan de Pruebas requieren ejecución completa y cobertura de módulos críticos, condiciones que no se "
     "satisfacen en el presente informe."),
    ("2. Las pruebas unitarias TDD del módulo de autenticación pasan al 100%.",
     "Los 16 tests de la suite actividad_tdd/ se ejecutaron sin fallos (0.001s). La lógica de registro, "
     "login, validación de email y contraseña, bloqueo por intentos y recuperación de contraseña funciona "
     "correctamente en el módulo UserManager (capa de dominio aislada)."),
    ("3. Se identificó un hallazgo técnico en el controlador de registro de la API real.",
     "El endpoint POST /api/usuarios/registro retorna HTTP 200 en lugar de HTTP 400/409 cuando el correo "
     "ya está registrado. Este comportamiento contradice el estándar REST y el resultado esperado del "
     "caso CP-HU01-004. No es un fallo en las pruebas TDD ejecutadas, sino un hallazgo de revisión estática."),
    ("4. El sistema tiene datos reales en la base de datos, lo que confirma uso previo funcional.",
     "La inspección de futbolzone.db reveló 5 usuarios registrados, 3 canchas activas y 8 reservas "
     "con distintos estados (completada, confirmada, pendiente), lo que indica que el flujo básico de "
     "reservas funcionó en algún momento del desarrollo."),
    ("5. 56 casos funcionales críticos permanecen sin ejecutar.",
     "Los módulos de Reservas, Canchas, Administración, Reportes, Personal, Agendamiento y la mayor "
     "parte de Seguridad y UI/UX no tienen resultados de ejecución. FutbolZone no puede considerarse "
     "verificado ni libre de defectos hasta completar este ciclo."),
    ("6. Los 10 casos de funcionalidades futuras son No Aplicables por diseño.",
     "Las historias HU-16 a HU-20 y HU-35 a HU-38 corresponden a un Roadmap de desarrollo que aún "
     "no tiene implementación en el código fuente. Los casos asociados se documentaron como "
     "especificación técnica para Sprints futuros."),
]

for titulo, detalle in conclusiones:
    story.append(P(f"<b>{titulo}</b>"))
    story.append(P(detalle))
    story.append(SP(0.1))

# ─── 19. RECOMENDACIONES ──────────────────────────────────────────────────
story.append(P("19. RECOMENDACIONES", h1))
story.append(hr(NAVY, 1.5))

recomendaciones = [
    ("P1 — INMEDIATA", "Corregir el hallazgo HLZ-001",
     "Modificar backend/app/controllers/usuario_controller.py para lanzar HTTPException(status_code=409, detail='El correo ya está registrado') en lugar de retornar api_response con HTTP 200."),
    ("P1 — INMEDIATA", "Programar y ejecutar el Ciclo 2 de pruebas manuales",
     "Iniciar el sistema completo (backend + frontend), ejecutar los 56 casos pendientes usando Postman/Bruno para las API REST y el navegador para los flujos de UI, y diligenciar los campos Resultado Obtenido, Estado y Observación en la columna G, H, I de la matriz."),
    ("P2 — CORTO PLAZO", "Implementar pruebas de integración con pytest + FastAPI TestClient",
     "Crear un archivo backend/tests/test_api.py usando from fastapi.testclient import TestClient y una base de datos SQLite en memoria para ejecutar pruebas automatizadas contra los endpoints reales sin depender de un servidor corriendo."),
    ("P2 — CORTO PLAZO", "Conectar TorneosView.tsx a la API real de torneos",
     "Reemplazar la lógica de localStorage en frontend/src/views/TorneosView.tsx por llamadas axios a /api/torneos/, /api/torneos/{id}/inscribirse, y ejecutar los 6 casos de prueba del módulo Torneos."),
    ("P3 — MEDIANO PLAZO", "Implementar pruebas de rendimiento",
     "Usar Locust o k6 para simular 50 usuarios concurrentes realizando reservas simultáneas y verificar que el sistema mantiene tiempos de respuesta aceptables y la prevención de solapamientos funciona bajo carga."),
    ("P3 — MEDIANO PLAZO", "Configurar pipeline de CI con ejecución automática de pruebas",
     "Crear .github/workflows/test.yml para ejecutar la suite TDD y las pruebas de integración pytest automáticamente en cada push o Pull Request, garantizando regresión continua."),
    ("P4 — LARGO PLAZO", "Planificar el Sprint de funcionalidades futuras",
     "Priorizar la implementación de HU-16 (Pasarela de Pagos) y HU-38 (Auditoría de Cambios) como las de mayor prioridad en el backlog, utilizando los casos CP-HU16 y CP-HU38 ya diseñados como criterios de aceptación."),
]

for prioridad, titulo, detalle in recomendaciones:
    color = "FAIL_R" if "INMEDIATA" in prioridad else ("AMBER" if "CORTO" in prioridad else "GRAY_TXT")
    story.append(P(
        f'<font color="#991B1B"><b>[{prioridad}]</b></font> <b>{titulo}</b>'
        if "INMEDIATA" in prioridad
        else f'<font color="#92400E"><b>[{prioridad}]</b></font> <b>{titulo}</b>'
        if "CORTO" in prioridad
        else f'<b>[{prioridad}]</b> <b>{titulo}</b>'
    ))
    story.append(P(detalle))
    story.append(SP(0.1))

# ─── 20. ANEXOS ───────────────────────────────────────────────────────────
story.append(P("20. ANEXOS", h1))
story.append(hr(NAVY, 1.5))
anex_rows = [
    ["Anexo", "Descripción", "Archivo / Ubicación"],
    ["A", "Matriz de Casos de Prueba actualizada con columnas de ejecución (G: Resultado, H: Estado, I: Observación)",
     "matriz-casos-de-prueba-futzone.xlsx (directorio raíz del proyecto)"],
    ["B", "Plan de Pruebas aprobado (alcance, estrategia, criterios de entrada/salida, riesgos)",
     "Plan_de_Pruebas_FutbolZone.pdf (directorio raíz del proyecto)"],
    ["C", "Informe de Laboratorio TDD — Ciclo Rojo-Verde-Refactorizar",
     "actividad_tdd/INFORME_EVIDENCIA_TDD.md"],
    ["D", "Suite de pruebas unitarias TDD — Autenticación (14 tests)",
     "actividad_tdd/test_auth.py"],
    ["E", "Suite de pruebas unitarias TDD — Interfaz CLI (2 tests)",
     "actividad_tdd/test_ui.py"],
    ["F", "Módulo de lógica de autenticación bajo TDD",
     "actividad_tdd/auth.py"],
    ["G", "Código fuente del controlador de usuarios (hallazgo HLZ-001 en L68)",
     "backend/app/controllers/usuario_controller.py"],
    ["H", "Base de datos del proyecto (consulta directa verificada)",
     "backend/futbolzone.db"],
    ["I", "Backlog de Historias de Usuario HU-01 a HU-38",
     "Backlog_FutbolZone_Navegable.xlsx"],
]
anex_t = Table(anex_rows, colWidths=[1.2*cm, 8.5*cm, 7.3*cm])
anex_t.setStyle(table_style_base())
story.append(anex_t)

story.append(SP(0.5))
story.append(hr(NAVY, 1))
story.append(P(
    "Informe elaborado por: Nicolas Felipe Paz Ortiz — Aprendiz ADSO / QA Tester | "
    "FutbolZone — SENA ADSO | Fecha: 10 de noviembre de 2026",
    S("footer2", fontName="Helvetica-Oblique", fontSize=8, textColor=GRAY_TXT,
      alignment=TA_CENTER, leading=12)))

# ─── BUILD PDF ────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title="Informe de Ejecucion de Pruebas — FutbolZone",
    author="Nicolas Felipe Paz Ortiz",
    subject="ISO/IEC/IEEE 29119-3:2021 — Test Execution Report",
    creator="ReportLab 5.1.0",
)

doc.build(story,
          onFirstPage=first_page,
          onLaterPages=later_pages)

print(f"PDF generado exitosamente: {OUTPUT_FILE}")
