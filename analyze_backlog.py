import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb1 = openpyxl.load_workbook('Backlog_FutbolZone_Navegable.xlsx', data_only=True)
wb2 = openpyxl.load_workbook('Historias_De_Usuario_FutbolZone_ADSO.xlsx', data_only=True)

print("=== COMPARISON BETWEEN FILES ===")
for sheetname in wb1.sheetnames:
    s1 = list(wb1[sheetname].iter_rows(values_only=True))
    s2 = list(wb2[sheetname].iter_rows(values_only=True))
    diffs = 0
    for r_idx in range(max(len(s1), len(s2))):
        r1 = s1[r_idx] if r_idx < len(s1) else None
        r2 = s2[r_idx] if r_idx < len(s2) else None
        if r1 != r2:
            diffs += 1
            if diffs <= 3:
                print(f"Diff in {sheetname} row {r_idx}: {r1} vs {r2}")
    print(f"Sheet '{sheetname}': rows={len(s1)} vs {len(s2)}, total differences = {diffs}")

print("\n=== DETAILED BACKLOG GENERAL CONTENT ===")
sheet = wb1['📋 Backlog General']
for i, row in enumerate(sheet.iter_rows(values_only=True)):
    # print headers and non-empty rows
    if any(row):
        print(f"Row {i:02d}: {row}")
