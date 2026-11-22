import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('Backlog_FutbolZone_Navegable.xlsx', data_only=True)
sheet = wb['📋 Backlog General']

header = None
hus = []
for i, row in enumerate(sheet.iter_rows(values_only=True)):
    if row[1] == 'ID':
        header = [str(c).strip() if c is not None else '' for c in row[1:]]
        continue
    if header and row[1] and str(row[1]).startswith('HU-'):
        item = {header[k]: row[k+1] for k in range(len(header)) if k+1 < len(row)}
        hus.append(item)

print(f"Total HUs found: {len(hus)}")
for hu in hus:
    print(f"{hu.get('ID')}: [{hu.get('Estado')}] [{hu.get('% Avance')}] {hu.get('Título de la Historia')} | Rol: {hu.get('Rol Asignado')} | Mod: {hu.get('Módulo')} | EP: {hu.get('Endpoint API Backend')} | Comp: {hu.get('Componente Frontend')}")
