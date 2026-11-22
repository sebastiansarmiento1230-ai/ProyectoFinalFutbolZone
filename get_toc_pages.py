import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader('Plan_de_Pruebas_FutbolZone.pdf')
print('Total pages:', len(reader.pages))

sections = [
    ('1. Identificación del Documento y Control de Cambios', '1. IDENTIFICACIÓN'),
    ('2. Introducción y Contexto del Proyecto', '2. INTRODUCCIÓN'),
    ('3. Propósito del Plan de Pruebas', '3. PROPÓSITO'),
    ('4. Alcance de las Pruebas (Test Scope)', '4. ALCANCE'),
    ('5. Objetivos Generales y Específicos de Calidad', '5. OBJETIVOS'),
    ('6. Referencias Documentales y Observación Normativa ISO 29119-3', '6. REFERENCIAS'),
    ('7. Descripción General de la Arquitectura del Sistema', '7. DESCRIPCIÓN'),
    ('8. Componentes y Módulos del Sistema Bajo Prueba', '8. COMPONENTES'),
    ('9. Funcionalidades Incluidas en el Alcance (In-Scope: 29 HUs)', '9. FUNCIONALIDADES INCLUIDAS'),
    ('10. Funcionalidades Excluidas o Pendientes (Out-of-Scope: 9 HUs)', '10. FUNCIONALIDADES EXCLUIDAS'),
    ('11. Estrategia y Niveles de Prueba (Pirámide de Pruebas ISO 29119-2)', '11. ESTRATEGIA'),
    ('12. Tipos de Pruebas Aplicables al Sistema', '12. TIPOS DE PRUEBAS'),
    ('13. Técnicas de Diseño de Pruebas (ISO/IEC/IEEE 29119-4)', '13. TÉCNICAS'),
    ('14. Entorno de Pruebas, Configuración y Herramientas', '14. ENTORNO'),
    ('15. Datos de Prueba y Consideraciones de Seguridad', '15. DATOS'),
    ('16. Roles, Responsabilidades y Matriz RACI', '16. ROLES'),
    ('17. Criterios de Entrada (Entry Criteria)', '17. CRITERIOS DE ENTRADA'),
    ('18. Criterios de Salida (Exit Criteria)', '18. CRITERIOS DE SALIDA'),
    ('19. Criterios de Suspensión y Reanudación (Approval/Rejection)', '19. CRITERIOS DE APROBACIÓN'),
    ('20. Gestión de Defectos, Ciclo de Vida y Plantilla de Incidencias', '20. GESTIÓN DE DEFECTOS'),
    ('21. Matriz de Riesgos Técnicos, Funcionales y Mitigación', '21. MATRIZ DE RIESGOS'),
    ('22. Cronograma y Secuencia Metodológica de Actividades', '22. CRONOGRAMA'),
    ('23. Entregables del Proceso de Pruebas (Test Deliverables)', '23. ENTREGABLES'),
    ('24. Aprobación del Plan de Pruebas y Firmas Institucionales', '24. APROBACIÓN'),
    ('25. Anexo Técnico: Observaciones Documentales e Inconsistencias', '25. ANEXO TÉCNICO')
]

for label, phrase in sections:
    p_num = None
    for idx in range(2, len(reader.pages)):
        txt = reader.pages[idx].extract_text()
        if phrase in txt:
            p_num = idx + 1
            break
    print(f'        ["{label}", "{p_num}"],')
