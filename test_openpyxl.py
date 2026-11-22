# Verification of openpyxl availability
import openpyxl
wb = openpyxl.Workbook()
print("openpyxl is ready. Active sheet:", wb.active.title)
