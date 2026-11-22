# -*- coding: utf-8 -*-
"""
Script generador de la Matriz de Casos de Prueba para FutbolZone
Archivo generado: matriz-casos-de-prueba-futzone.xlsx
Norma de referencia: ISO/IEC/IEEE 29119-3:2021 (Apartado 7.3.5)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from casos_data import CASOS_PRUEBA
from collections import Counter

def create_test_matrix():
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles definition
    FONT_FAMILY = "Calibri"
    
    # Palette
    NAVY_HEADER = "1B365D"       # Deep Navy
    SLATE_HEADER = "2C3E50"      # Slate Dark
    TEAL_HEADER = "0E7490"       # Deep Teal
    ACCENT_BLUE = "2563EB"       # Royal Blue
    ACCENT_LIGHT = "EFF6FF"      # Very light blue for zebra / cards
    ZEBRA_FILL = "F8FAFC"        # Light gray-blue
    BORDER_COLOR = "CBD5E1"      # Light border slate
    KPI_BG_1 = "EFF6FF"          # Blue light
    KPI_BG_2 = "F0FDF4"          # Green light
    KPI_BG_3 = "FFFBEB"          # Amber light
    KPI_BG_4 = "FEF2F2"          # Red light

    font_header = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
    font_sub_header = Font(name=FONT_FAMILY, size=10, bold=True, color="1E293B")
    font_data = Font(name=FONT_FAMILY, size=9.5, color="1E293B")
    font_bold = Font(name=FONT_FAMILY, size=9.5, bold=True, color="0F172A")
    font_italic = Font(name=FONT_FAMILY, size=9, italic=True, color="64748B")
    
    font_title = Font(name=FONT_FAMILY, size=16, bold=True, color="1B365D")
    font_subtitle = Font(name=FONT_FAMILY, size=11, italic=True, color="475569")
    font_section = Font(name=FONT_FAMILY, size=12, bold=True, color="1B365D")

    header_fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    table_header_fill = PatternFill(start_color=SLATE_HEADER, end_color=SLATE_HEADER, fill_type="solid")
    teal_header_fill = PatternFill(start_color=TEAL_HEADER, end_color=TEAL_HEADER, fill_type="solid")
    sub_header_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    zebra_fill = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    thin_border_side = Side(style='thin', color=BORDER_COLOR)
    card_border_side = Side(style='medium', color="94A3B8")
    
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=Side(style='medium', color="0F172A"))

    align_center = Alignment(horizontal="center", vertical="center")
    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_top_center = Alignment(horizontal="center", vertical="top")
    align_center_wrap = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # -------------------------------------------------------------------------
    # HOJA 1: CASOS DE PRUEBA (Exactamente 6 columnas obligatorias)
    # -------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="Casos de prueba")
    ws1.views.sheetView[0].showGridLines = True
    ws1.freeze_panes = "A2"

    h1_headers = [
        "ID",
        "Objetivo",
        "Precondiciones",
        "Entradas",
        "Resultados esperados",
        "Poscondición"
    ]

    ws1.append(h1_headers)
    ws1.row_dimensions[1].height = 28

    for col_idx, col_name in enumerate(h1_headers, start=1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = header_border

    for row_idx, caso in enumerate(CASOS_PRUEBA, start=2):
        row_values = [
            caso["id"],
            caso["objetivo"],
            caso["precondiciones"],
            caso["entradas"],
            caso["resultados_esperados"],
            caso["poscondicion"]
        ]
        ws1.append(row_values)
        
        # Calculate dynamic row height based on content line breaks
        max_lines = max(len(str(val).split("\n")) for val in row_values)
        calculated_height = max(24, min(140, max_lines * 16 + 10))
        ws1.row_dimensions[row_idx].height = calculated_height

        row_fill = white_fill if row_idx % 2 == 0 else zebra_fill

        for col_idx in range(1, 7):
            cell = ws1.cell(row=row_idx, column=col_idx)
            cell.font = font_bold if col_idx == 1 else font_data
            cell.fill = row_fill
            cell.border = cell_border
            if col_idx == 1:
                cell.alignment = align_top_center
            else:
                cell.alignment = align_top_left

    # Set column widths for Sheet 1
    col_widths_s1 = {
        "A": 16,  # ID
        "B": 42,  # Objetivo
        "C": 36,  # Precondiciones
        "D": 45,  # Entradas
        "E": 48,  # Resultados esperados
        "F": 34   # Poscondicion
    }
    for col_letter, width in col_widths_s1.items():
        ws1.column_dimensions[col_letter].width = width

    ws1.auto_filter.ref = f"A1:F{len(CASOS_PRUEBA) + 1}"

    # -------------------------------------------------------------------------
    # HOJA 2: TRAZABILIDAD
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Trazabilidad")
    ws2.views.sheetView[0].showGridLines = True
    ws2.freeze_panes = "A2"

    h2_headers = [
        "ID del caso de prueba",
        "ID de historia de usuario",
        "Nombre de la historia",
        "Módulo",
        "Prioridad",
        "Estado de implementación identificado",
        "Observaciones"
    ]

    ws2.append(h2_headers)
    ws2.row_dimensions[1].height = 28

    for col_idx, col_name in enumerate(h2_headers, start=1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = header_fill
        cell.alignment = align_center
        cell.border = header_border

    # Status color highlights
    fill_impl = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")     # Light green
    fill_parc = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")     # Light amber
    fill_pend = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")     # Light red
    font_status_impl = Font(name=FONT_FAMILY, size=9.5, bold=True, color="166534")
    font_status_parc = Font(name=FONT_FAMILY, size=9.5, bold=True, color="92400E")
    font_status_pend = Font(name=FONT_FAMILY, size=9.5, bold=True, color="991B1B")

    for row_idx, caso in enumerate(CASOS_PRUEBA, start=2):
        row_values = [
            caso["id"],
            caso["hu_id"],
            caso["hu_titulo"],
            caso["modulo"],
            caso["prioridad"],
            caso["estado_impl"],
            caso["observaciones"]
        ]
        ws2.append(row_values)
        ws2.row_dimensions[row_idx].height = 24

        row_fill = white_fill if row_idx % 2 == 0 else zebra_fill

        for col_idx in range(1, 8):
            cell = ws2.cell(row=row_idx, column=col_idx)
            cell.font = font_bold if col_idx in (1, 2) else font_data
            cell.fill = row_fill
            cell.border = cell_border
            
            if col_idx in (1, 2, 5):
                cell.alignment = align_top_center
            elif col_idx == 6:
                cell.alignment = align_top_center
                # Custom status pill styling
                st = caso["estado_impl"]
                if "Implementada" in st and "Parcial" not in st:
                    cell.fill = fill_impl
                    cell.font = font_status_impl
                elif "Parcial" in st:
                    cell.fill = fill_parc
                    cell.font = font_status_parc
                else:
                    cell.fill = fill_pend
                    cell.font = font_status_pend
            else:
                cell.alignment = align_top_left

    col_widths_s2 = {
        "A": 18,  # ID caso
        "B": 14,  # ID HU
        "C": 35,  # Nombre historia
        "D": 18,  # Modulo
        "E": 14,  # Prioridad
        "F": 30,  # Estado impl
        "G": 48   # Observaciones
    }
    for col_letter, width in col_widths_s2.items():
        ws2.column_dimensions[col_letter].width = width

    ws2.auto_filter.ref = f"A1:G{len(CASOS_PRUEBA) + 1}"

    # -------------------------------------------------------------------------
    # HOJA 3: RESUMEN EJECUTIVO DE DISEÑO DE PRUEBAS
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="Resumen")
    ws3.views.sheetView[0].showGridLines = True
    ws3.freeze_panes = "A5"

    # Title Block
    ws3.merge_cells("A1:G1")
    title_cell = ws3["A1"]
    title_cell.value = "FUTBOLZONE — RESUMEN EJECUTIVO DE DISEÑO DE PRUEBAS"
    title_cell.font = font_title
    title_cell.alignment = Alignment(horizontal="left", vertical="center")
    ws3.row_dimensions[1].height = 32

    ws3.merge_cells("A2:G2")
    sub_cell = ws3["A2"]
    sub_cell.value = "Norma ISO/IEC/IEEE 29119-3:2021 | Especificación de Casos de Prueba (Apartado 7.3.5) | Sin Métricas de Ejecución (Fase de Diseño)"
    sub_cell.font = font_subtitle
    sub_cell.alignment = Alignment(horizontal="left", vertical="center")
    ws3.row_dimensions[2].height = 20

    ws3.row_dimensions[3].height = 10  # blank space

    # KPI Summary Cards Block (Row 4 & 5)
    # Total Casos, Casos Implementados, Casos Parciales, Casos Futuros/Pendientes
    total_casos = len(CASOS_PRUEBA)
    casos_impl = sum(1 for c in CASOS_PRUEBA if c["estado_impl"] == "Implementada")
    casos_parc = sum(1 for c in CASOS_PRUEBA if "Parcial" in c["estado_impl"])
    casos_pend = sum(1 for c in CASOS_PRUEBA if "Pendiente" in c["estado_impl"] or "Fuera" in c["estado_impl"])

    kpis = [
        ("A4:B4", "A5:B5", "TOTAL CASOS DISEÑADOS", str(total_casos), "EFF6FF", "1E40AF"),
        ("C4:C4", "C5:C5", "CASOS IMPLEMENTADOS (VERIFICABLES)", str(casos_impl), "DCFCE7", "166534"),
        ("D4:E4", "D5:E5", "CASOS PARCIALES (BACKEND OK / UI MOCK)", str(casos_parc), "FEF3C7", "92400E"),
        ("F4:G4", "F5:G5", "CASOS FUTUROS (ROADMAP / PENDIENTES)", str(casos_pend), "FEE2E2", "991B1B"),
    ]

    ws3.row_dimensions[4].height = 18
    ws3.row_dimensions[5].height = 30

    for title_range, val_range, kpi_title, kpi_val, bg_color, text_color in kpis:
        # Title merge
        ws3.merge_cells(title_range)
        t_cell = ws3[title_range.split(":")[0]]
        t_cell.value = kpi_title
        t_cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="475569")
        t_cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
        t_cell.alignment = align_center

        # Value merge
        ws3.merge_cells(val_range)
        v_cell = ws3[val_range.split(":")[0]]
        v_cell.value = kpi_val
        v_cell.font = Font(name=FONT_FAMILY, size=18, bold=True, color=text_color)
        v_cell.fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
        v_cell.alignment = align_center

        # Apply borders to range
        cells_in_card = ws3[title_range.split(":")[0]: val_range.split(":")[1]]
        for row in cells_in_card:
            for c in row:
                c.border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    ws3.row_dimensions[6].height = 15  # spacer

    current_row = 7

    # -------------------------------------------------------------------------
    # TABLA 1: DISTRIBUCIÓN DE CASOS POR MÓDULO FUNCIONAL
    # -------------------------------------------------------------------------
    ws3.cell(row=current_row, column=1, value="1. DISTRIBUCIÓN DE CASOS DE PRUEBA POR MÓDULO FUNCIONAL").font = font_section
    current_row += 1

    t1_headers = ["Módulo del Sistema", "Cantidad de Casos", "% del Total", "Nivel de Prueba Predominante", "Estado Técnico Predominante"]
    ws3.row_dimensions[current_row].height = 24
    for c_idx, h in enumerate(t1_headers, start=1):
        c = ws3.cell(row=current_row, column=c_idx, value=h)
        c.font = font_header
        c.fill = table_header_fill
        c.alignment = align_center
        c.border = header_border
    current_row += 1

    modulos_counter = Counter(c["modulo"] for c in CASOS_PRUEBA)
    modulo_info = {
        "Reservas": ("Pruebas Funcionales / API REST / Lógica de Cruce", "Implementado (CRUD + Validaciones de solapamiento)"),
        "Seguridad": ("Pruebas de Seguridad / JWT / RBAC / Autorización", "Implementado (Roles Cliente/Admin + Protección de rutas)"),
        "Canchas": ("Pruebas Funcionales / Catálogo / Filtros / Administración", "Implementado (CRUD canchas, tipos f5/f7/f11, fotos)"),
        "Torneos": ("Pruebas de Integración / Estado de Inscripciones", "Parcial (API FastAPI lista; Frontend con Mock LocalStorage)"),
        "Autenticación": ("Pruebas de Registro / Login / Hash Bcrypt", "Implementado (Endpoints /registro, /login funcionales)"),
        "Agendamiento": ("Pruebas de Cálculo de Tarifas y Disponibilidad", "Implementado (Algoritmo de cálculo de precio dinámico)"),
        "UI / UX": ("Pruebas de Interfaz / Tema Oscuro-Claro / Responsive", "Implementado (Context API React + Tailwind CSS)"),
        "Personal": ("Pruebas de Gestión de Empleados / Permisos", "Implementado (CRUD empleados con rol admin restringido)"),
        "Reportes": ("Pruebas de Métricas / Exportación CSV y PDF", "Implementado (Endpoints de estadísticas y descarga)"),
        "Administración": ("Pruebas de Dashboard / Métricas de Ocupación", "Implementado (Dashboard con tarjetas y gráficos de control)"),
        "Pagos": ("Pruebas de Integración con Pasarela (Wompi / PayU)", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
        "Comprobantes": ("Pruebas de Generación PDF y Código QR de Reserva", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
        "Notificaciones": ("Pruebas de Disparo de Recordatorios SMS/WhatsApp", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
        "Fidelización": ("Pruebas de Reglas de Acumulación y Canje de Puntos", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
        "Integraciones": ("Pruebas de Sincronización Google Calendar API", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
        "DevOps": ("Pruebas de Pipeline CI/CD y Healthcheck Cloud", "Pendiente / Roadmap Futuro (0% código backend/frontend)"),
    }

    start_t1 = current_row
    for mod, count in modulos_counter.most_common():
        pct = (count / total_casos) * 100
        nivel, estado_tec = modulo_info.get(mod, ("Pruebas Funcionales", "Implementado"))
        
        ws3.cell(row=current_row, column=1, value=mod).font = font_bold
        ws3.cell(row=current_row, column=2, value=count).alignment = align_top_center
        ws3.cell(row=current_row, column=3, value=f"{pct:.1f}%").alignment = align_top_center
        ws3.cell(row=current_row, column=4, value=nivel).alignment = align_top_left
        ws3.cell(row=current_row, column=5, value=estado_tec).alignment = align_top_left

        for c_idx in range(1, 6):
            cell = ws3.cell(row=current_row, column=c_idx)
            cell.border = cell_border
            cell.font = font_data if c_idx > 1 else font_bold
            cell.fill = white_fill if current_row % 2 == 0 else zebra_fill

        ws3.row_dimensions[current_row].height = 20
        current_row += 1

    # Total Row Table 1
    ws3.cell(row=current_row, column=1, value="TOTAL GENERAL").font = font_header
    ws3.cell(row=current_row, column=1).fill = sub_header_fill
    ws3.cell(row=current_row, column=2, value=total_casos).font = font_bold
    ws3.cell(row=current_row, column=2).alignment = align_top_center
    ws3.cell(row=current_row, column=2).fill = sub_header_fill
    ws3.cell(row=current_row, column=3, value="100.0%").font = font_bold
    ws3.cell(row=current_row, column=3).alignment = align_top_center
    ws3.cell(row=current_row, column=3).fill = sub_header_fill
    ws3.cell(row=current_row, column=4, value="Cobertura Multi-nivel (Unitario, API, Integración, UI)").font = font_italic
    ws3.cell(row=current_row, column=4).fill = sub_header_fill
    ws3.cell(row=current_row, column=5, value="75.0% Verificable / 25.0% Roadmap").font = font_italic
    ws3.cell(row=current_row, column=5).fill = sub_header_fill
    for c_idx in range(1, 6):
        ws3.cell(row=current_row, column=c_idx).border = header_border
    ws3.row_dimensions[current_row].height = 22
    current_row += 2

    # -------------------------------------------------------------------------
    # TABLA 2: DISTRIBUCIÓN POR NATURALEZA DEL ESCENARIO (POSITIVOS VS NEGATIVOS/BORDES)
    # -------------------------------------------------------------------------
    ws3.cell(row=current_row, column=1, value="2. DISTRIBUCIÓN POR NATURALEZA DE LA PRUEBA (TÉCNICAS DE DISEÑO)").font = font_section
    current_row += 1

    t2_headers = ["Tipo de Escenario", "Cantidad de Casos", "% del Total", "Técnicas de Diseño Aplicadas", "Propósito en el Aseguramiento de Calidad"]
    ws3.row_dimensions[current_row].height = 24
    for c_idx, h in enumerate(t2_headers, start=1):
        c = ws3.cell(row=current_row, column=c_idx, value=h)
        c.font = font_header
        c.fill = teal_header_fill
        c.alignment = align_center
        c.border = header_border
    current_row += 1

    pos_count = sum(1 for c in CASOS_PRUEBA if c["tipo"] == "Positivo")
    neg_count = sum(1 for c in CASOS_PRUEBA if c["tipo"] == "Negativo")

    scenarios = [
        (
            "Escenarios Positivos (Caminos Felices)",
            pos_count,
            f"{(pos_count/total_casos)*100:.1f}%",
            "Partición de equivalencia válida, flujos estándar, validación de lógica de negocio exitosa.",
            "Comprobar que el software cumple con los requisitos funcionales especificados bajo datos de entrada conformes."
        ),
        (
            "Escenarios Negativos / Bordes / Excepciones",
            neg_count,
            f"{(neg_count/total_casos)*100:.1f}%",
            "Análisis de valores límite (BVA), transiciones de estado inválidas, tablas de decisión de conflicto, inyección de tokens expirados.",
            "Evaluar la robustez del sistema, prevención de estados inconsistentes, control de errores HTTP (400, 401, 403, 404, 409, 422) y seguridad."
        )
    ]

    for title, cnt, pct, tecnicas, proposito in scenarios:
        ws3.cell(row=current_row, column=1, value=title).font = font_bold
        ws3.cell(row=current_row, column=2, value=cnt).alignment = align_top_center
        ws3.cell(row=current_row, column=3, value=pct).alignment = align_top_center
        ws3.cell(row=current_row, column=4, value=tecnicas).alignment = align_top_left
        ws3.cell(row=current_row, column=5, value=proposito).alignment = align_top_left

        for c_idx in range(1, 6):
            cell = ws3.cell(row=current_row, column=c_idx)
            cell.border = cell_border
            cell.font = font_data if c_idx > 1 else font_bold
            cell.fill = white_fill if current_row % 2 == 0 else zebra_fill

        ws3.row_dimensions[current_row].height = 36
        current_row += 1

    # Total Row Table 2
    ws3.cell(row=current_row, column=1, value="TOTAL GENERAL").font = font_header
    ws3.cell(row=current_row, column=1).fill = sub_header_fill
    ws3.cell(row=current_row, column=2, value=total_casos).font = font_bold
    ws3.cell(row=current_row, column=2).alignment = align_top_center
    ws3.cell(row=current_row, column=2).fill = sub_header_fill
    ws3.cell(row=current_row, column=3, value="100.0%").font = font_bold
    ws3.cell(row=current_row, column=3).alignment = align_top_center
    ws3.cell(row=current_row, column=3).fill = sub_header_fill
    ws3.cell(row=current_row, column=4, value="Cobertura balanceada 66.7% positivo / 33.3% robustez").font = font_italic
    ws3.cell(row=current_row, column=4).fill = sub_header_fill
    ws3.cell(row=current_row, column=5, value="Garantiza calidad funcional y tolerancia a fallos").font = font_italic
    ws3.cell(row=current_row, column=5).fill = sub_header_fill
    for c_idx in range(1, 6):
        ws3.cell(row=current_row, column=c_idx).border = header_border
    ws3.row_dimensions[current_row].height = 22
    current_row += 2

    # -------------------------------------------------------------------------
    # TABLA 3: COBERTURA DE HISTORIAS DE USUARIO (HU-01 a HU-38)
    # -------------------------------------------------------------------------
    ws3.cell(row=current_row, column=1, value="3. COBERTURA GLOBAL DE HISTORIAS DE USUARIO (HU-01 a HU-38)").font = font_section
    current_row += 1

    t3_headers = ["Categoría de Cobertura", "Historias de Usuario Cubiertas", "Cantidad de HUs", "% de HUs", "Casos Diseñados", "Acción de QA Recomendada"]
    ws3.row_dimensions[current_row].height = 24
    for c_idx, h in enumerate(t3_headers, start=1):
        c = ws3.cell(row=current_row, column=c_idx, value=h)
        c.font = font_header
        c.fill = table_header_fill
        c.alignment = align_center
        c.border = header_border
    current_row += 1

    hu_stats = [
        (
            "Historias Implementadas (Verificables en Código)",
            "HU-01 a HU-10, HU-13 a HU-15, HU-21 a HU-32, HU-34",
            26,
            "68.4%",
            casos_impl,
            "Ejecución inmediata en ciclo de pruebas de aceptación y regresión."
        ),
        (
            "Historias Parcialmente Implementadas",
            "HU-11, HU-12, HU-33 (Torneos)",
            3,
            "7.9%",
            casos_parc,
            "Ejecutar pruebas en API REST (/api/torneos); reportar desacoplamiento de TorneosView.tsx (mock LocalStorage)."
        ),
        (
            "Historias Futuras / Pendientes (Roadmap)",
            "HU-16 a HU-20, HU-35 a HU-38",
            9,
            "23.7%",
            casos_pend,
            "Casos pre-diseñados como especificación técnica para desarrollo en Sprint futuro. Fuera del ciclo ejecutable actual."
        ),
    ]

    for cat, hus_text, qty, pct, c_qty, accion in hu_stats:
        ws3.cell(row=current_row, column=1, value=cat).font = font_bold
        ws3.cell(row=current_row, column=2, value=hus_text).alignment = align_top_left
        ws3.cell(row=current_row, column=3, value=qty).alignment = align_top_center
        ws3.cell(row=current_row, column=4, value=pct).alignment = align_top_center
        ws3.cell(row=current_row, column=5, value=c_qty).alignment = align_top_center
        ws3.cell(row=current_row, column=6, value=accion).alignment = align_top_left

        for c_idx in range(1, 7):
            cell = ws3.cell(row=current_row, column=c_idx)
            cell.border = cell_border
            cell.font = font_data if c_idx not in (1, 3, 5) else font_bold
            cell.fill = white_fill if current_row % 2 == 0 else zebra_fill

        ws3.row_dimensions[current_row].height = 28
        current_row += 1

    # Total Row Table 3
    ws3.cell(row=current_row, column=1, value="TOTAL HISTORIAS DE USUARIO").font = font_header
    ws3.cell(row=current_row, column=1).fill = sub_header_fill
    ws3.cell(row=current_row, column=2, value="HU-01 a HU-38 (Backlog Navegable Completo)").font = font_bold
    ws3.cell(row=current_row, column=2).fill = sub_header_fill
    ws3.cell(row=current_row, column=3, value=38).font = font_bold
    ws3.cell(row=current_row, column=3).alignment = align_top_center
    ws3.cell(row=current_row, column=3).fill = sub_header_fill
    ws3.cell(row=current_row, column=4, value="100.0%").font = font_bold
    ws3.cell(row=current_row, column=4).alignment = align_top_center
    ws3.cell(row=current_row, column=4).fill = sub_header_fill
    ws3.cell(row=current_row, column=5, value=total_casos).font = font_bold
    ws3.cell(row=current_row, column=5).alignment = align_top_center
    ws3.cell(row=current_row, column=5).fill = sub_header_fill
    ws3.cell(row=current_row, column=6, value="100% Cobertura de especificación según ISO/IEC/IEEE 29119-3").font = font_italic
    ws3.cell(row=current_row, column=6).fill = sub_header_fill
    for c_idx in range(1, 7):
        ws3.cell(row=current_row, column=c_idx).border = header_border
    ws3.row_dimensions[current_row].height = 22
    current_row += 2

    # -------------------------------------------------------------------------
    # TABLA 4: DETALLE DE HISTORIAS DE USUARIO PENDIENTES / ROADMAP (0% EN CÓDIGO)
    # -------------------------------------------------------------------------
    ws3.cell(row=current_row, column=1, value="4. DETALLE DE HISTORIAS DE USUARIO PENDIENTES DE IMPLEMENTACIÓN (ROADMAP FUTURO)").font = font_section
    current_row += 1

    t4_headers = ["ID Historia", "Nombre de la Historia", "Módulo", "Prioridad", "Casos Asociados", "Causa Técnica de No Ejecución"]
    ws3.row_dimensions[current_row].height = 24
    for c_idx, h in enumerate(t4_headers, start=1):
        c = ws3.cell(row=current_row, column=c_idx, value=h)
        c.font = font_header
        c.fill = table_header_fill
        c.alignment = align_center
        c.border = header_border
    current_row += 1

    pending_hus = [
        ("HU-16", "Pasarela de Pagos en Línea", "Pagos", "Alta", "CP-HU16-001, CP-HU16-002", "Sin pasarela integrada en backend (Wompi/PayU); no existen tablas de transacciones bancarias."),
        ("HU-17", "Generación de Comprobantes PDF con QR", "Comprobantes", "Media", "CP-HU17-001", "Falta librería de generación de PDF en backend (ReportLab) y generador de códigos QR para reservas."),
        ("HU-18", "Recordatorios por SMS o WhatsApp", "Notificaciones", "Baja", "CP-HU18-001", "Sin servicio de mensajería (Twilio / Meta Graph API); no hay workers asíncronos programados."),
        ("HU-19", "Sistema de Fidelización y Puntos", "Fidelización", "Baja", "CP-HU19-001", "El modelo de datos no cuenta con tabla 'puntos' ni reglas de acumulación/redención en negocio."),
        ("HU-20", "Sincronización con Google Calendar", "Integraciones", "Baja", "CP-HU20-001", "Sin integración OAuth2 de Google ni endpoints de sincronización iCal/Google Calendar API."),
        ("HU-35", "Cuadros de Eliminatorias de Torneos", "Torneos", "Baja", "CP-HU35-001", "No existe motor de emparejamiento de llaves ni visualizador gráfico de brackets de torneo."),
        ("HU-36", "Lector y Validación de QR en Recepción", "Comprobantes", "Media", "CP-HU36-001", "No existe componente lector de cámara de código QR en frontend ni endpoint de canje en backend."),
        ("HU-37", "Despliegue Continuo Cloud y Monitor", "DevOps", "Media", "CP-HU37-001", "Sin pipelines de GitHub Actions configurados ni contenedor Dockerfile optimizado para producción."),
        ("HU-38", "Auditoría de Cambios y Logs Administrativos", "Seguridad", "Alta", "CP-HU38-001", "No existe tabla de 'auditoria_logs' en BD ni middleware de trazabilidad de cambios en FastAPI."),
    ]

    for hu_id, hu_nom, mod, prio, casos_str, causa in pending_hus:
        ws3.cell(row=current_row, column=1, value=hu_id).font = font_bold
        ws3.cell(row=current_row, column=1).alignment = align_top_center
        ws3.cell(row=current_row, column=2, value=hu_nom).alignment = align_top_left
        ws3.cell(row=current_row, column=3, value=mod).alignment = align_top_center
        ws3.cell(row=current_row, column=4, value=prio).alignment = align_top_center
        ws3.cell(row=current_row, column=5, value=casos_str).alignment = align_top_center
        ws3.cell(row=current_row, column=6, value=causa).alignment = align_top_left

        for c_idx in range(1, 7):
            cell = ws3.cell(row=current_row, column=c_idx)
            cell.border = cell_border
            cell.font = font_data if c_idx not in (1, 4) else font_bold
            cell.fill = fill_pend if c_idx == 1 else (white_fill if current_row % 2 == 0 else zebra_fill)

        ws3.row_dimensions[current_row].height = 24
        current_row += 1

    # Column widths for Sheet 3
    col_widths_s3 = {
        "A": 16,
        "B": 38,
        "C": 18,
        "D": 16,
        "E": 28,
        "F": 46,
        "G": 20
    }
    for col_letter, width in col_widths_s3.items():
        ws3.column_dimensions[col_letter].width = width

    # Save workbook
    output_filename = "matriz-casos-de-prueba-futzone.xlsx"
    wb.save(output_filename)
    print(f"Archivo generado exitosamente: {output_filename}")

if __name__ == "__main__":
    create_test_matrix()
