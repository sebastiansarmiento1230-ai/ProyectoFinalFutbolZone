# -*- coding: utf-8 -*-
"""
Compilador Final del Plan de Pruebas de Software para FutbolZone
Genera: Plan_de_Pruebas_FutbolZone.pdf
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak
from pdf_core import NumberedCanvas

from part1_intro import get_part1_flowables
from part2_system import get_part2_flowables
from part3_strategy import get_part3_flowables
from part4_management import get_part4_flowables

def build_pdf():
    pdf_filename = "Plan_de_Pruebas_FutbolZone.pdf"
    
    # Márgenes de 40pt (aprox. 14mm), ancho imprimible = 532pt
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )
    
    story = []
    
    print("Agregando Parte 1: Portada, TOC, Identificación, Introducción, Propósito, Alcance, Objetivos...")
    story.extend(get_part1_flowables())
    
    print("Agregando Parte 2: Referencias, Descripción del Sistema, Módulos, In-Scope (29 HUs), Out-of-Scope (9 HUs)...")
    story.extend(get_part2_flowables())
    
    print("Agregando Parte 3: Estrategia y Niveles, Tipos de Pruebas, Técnicas ISO 29119-4, Entorno, Datos y RACI...")
    story.extend(get_part3_flowables())
    
    print("Agregando Parte 4: Criterios Entrada/Salida, Suspensión/Reanudación, Defectos, Riesgos, Cronograma, Entregables, Firmas y Anexo Inconsistencias...")
    story.extend(get_part4_flowables())
    
    print(f"Compilando documento final con NumberedCanvas: {pdf_filename}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    
    file_size_kb = os.path.getsize(pdf_filename) / 1024
    print(f"¡ÉXITO! Documento generado correctamente: {pdf_filename} ({file_size_kb:.1f} KB)")

if __name__ == "__main__":
    build_pdf()
