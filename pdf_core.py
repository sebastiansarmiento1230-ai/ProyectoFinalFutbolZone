# -*- coding: utf-8 -*-
"""
Generador del Plan Maestro de Pruebas de Software para FutbolZone
Norma ISO/IEC/IEEE 29119-3:2021
Archivo generado: Plan_de_Pruebas_FutbolZone.pdf
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ==============================================================================
# CANVAS DE DOS PASADAS (ENCABEZADO Y PIE DE PÁGINA)
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            
            # Encabezado (Header)
            self.setFont('Helvetica-Bold', 7.5)
            self.setFillColor(colors.HexColor('#0F2942'))
            self.drawString(40, letter[1] - 30, 'PLAN MAESTRO DE PRUEBAS DE SOFTWARE — FUTBOLZONE')
            
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#475569'))
            self.drawRightString(letter[0] - 40, letter[1] - 30, 'ISO/IEC/IEEE 29119-3:2021 | PLN-QA-FZ-2026-001')
            
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.6)
            self.line(40, letter[1] - 34, letter[0] - 40, letter[1] - 34)
            
            # Pie de página (Footer)
            self.setStrokeColor(colors.HexColor('#E2E8F0'))
            self.setLineWidth(0.6)
            self.line(40, 36, letter[0] - 40, 36)
            
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#64748B'))
            self.drawString(40, 25, 'SENA Centro de Formación | Programa ADSO | Aseguramiento de Calidad de Software')
            
            page_text = f'Página {self._pageNumber} de {page_count}'
            self.setFont('Helvetica-Bold', 7.5)
            self.setFillColor(colors.HexColor('#1E3A8A'))
            self.drawRightString(letter[0] - 40, 25, page_text)
            self.restoreState()


# ==============================================================================
# ESTILOS TIPOGRÁFICOS
# ==============================================================================
styles = getSampleStyleSheet()

NAVY_PRIMARY    = colors.HexColor('#0F2942') # Azul oscuro naval
BLUE_ACCENT     = colors.HexColor('#1E3A8A') # Azul corporativo
GREEN_ACCENT    = colors.HexColor('#047857') # Verde esmeralda cancha
TEXT_DARK       = colors.HexColor('#0F172A') # Casi negro
TEXT_MUTED      = colors.HexColor('#475569') # Gris texto
BG_LIGHT        = colors.HexColor('#F8FAFC') # Fondo gris neutro
BG_ROW_ALT      = colors.HexColor('#F1F5F9') # Fila alterna
BORDER_COLOR    = colors.HexColor('#CBD5E1') # Bordes de tabla
CALLOUT_INFO_BG = colors.HexColor('#EFF6FF')
CALLOUT_WARN_BG = colors.HexColor('#FFFBEB')
CALLOUT_WARN_BR = colors.HexColor('#D97706')
CALLOUT_DANG_BG = colors.HexColor('#FEF2F2')
CALLOUT_DANG_BR = colors.HexColor('#DC2626')

styles.add(ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=NAVY_PRIMARY, spaceAfter=6))
styles.add(ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=GREEN_ACCENT, spaceAfter=12))
styles.add(ParagraphStyle('SectionHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=NAVY_PRIMARY, spaceBefore=11, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle('SubsectionHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=12.5, textColor=BLUE_ACCENT, spaceBefore=7, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle('SubSubsectionHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=GREEN_ACCENT, spaceBefore=5, spaceAfter=2, keepWithNext=True))
styles.add(ParagraphStyle('BodyJustified', parent=styles['Normal'], fontName='Helvetica', fontSize=7.4, leading=10.2, textColor=TEXT_DARK, spaceAfter=3, alignment=4))
styles.add(ParagraphStyle('BodyBullet', parent=styles['Normal'], fontName='Helvetica', fontSize=7.4, leading=10.2, textColor=TEXT_DARK, leftIndent=9, firstLineIndent=-7, spaceAfter=2))
styles.add(ParagraphStyle('CalloutText', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.4, textColor=TEXT_DARK))
styles.add(ParagraphStyle('CalloutTextBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9.4, textColor=TEXT_DARK))
styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=colors.white, alignment=1))
styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=6.3, leading=8, textColor=TEXT_DARK))
styles.add(ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=6.3, leading=8, textColor=TEXT_DARK))
styles.add(ParagraphStyle('TableCellCenter', parent=styles['Normal'], fontName='Helvetica', fontSize=6.3, leading=8, textColor=TEXT_DARK, alignment=1))
styles.add(ParagraphStyle('TOCItem', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=NAVY_PRIMARY))
styles.add(ParagraphStyle('TOCPage', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=10.5, textColor=BLUE_ACCENT, alignment=2))

def create_callout(text, title=None, style_type="info", width=532):
    bg_map = {
        "info": (CALLOUT_INFO_BG, BLUE_ACCENT),
        "warning": (CALLOUT_WARN_BG, CALLOUT_WARN_BR),
        "danger": (CALLOUT_DANG_BG, CALLOUT_DANG_BR),
    }
    bg_col, border_col = bg_map.get(style_type, (CALLOUT_INFO_BG, BLUE_ACCENT))
    flowables = []
    if title:
        flowables.append(Paragraph(f"<b>{title}</b>", styles['CalloutTextBold']))
        flowables.append(Spacer(1, 1.5))
    flowables.append(Paragraph(text, styles['CalloutText']))
    t = Table([[flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_col),
        ('BOX', (0,0), (-1,-1), 1, border_col),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def create_table(header_data, rows_data, col_widths, align_cols=None):
    table_data = []
    h_row = [Paragraph(str(h), styles['TableHeader']) for h in header_data]
    table_data.append(h_row)
    for r_idx, row in enumerate(rows_data):
        row_cells = []
        for c_idx, val in enumerate(row):
            if isinstance(val, Paragraph):
                row_cells.append(val)
            else:
                align = 'TableCell'
                if align_cols and c_idx in align_cols:
                    align = align_cols[c_idx]
                row_cells.append(Paragraph(str(val), styles[align]))
        table_data.append(row_cells)
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    ts = [
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_ACCENT),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2.5),
    ]
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            ts.append(('BACKGROUND', (0, i), (-1, i), BG_ROW_ALT))
    t.setStyle(TableStyle(ts))
    return t

print("Base loaded successfully.")
