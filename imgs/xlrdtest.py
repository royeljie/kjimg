import xlrd

print(xlrd.__VERSION__)
xls = xlrd.open_workbook('')
sheet = xls.sheets()[0]
values = sheet.row_values(2)
print(values)
