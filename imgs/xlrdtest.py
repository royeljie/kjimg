import xlrd

print(xlrd.__VERSION__)
xls = xlrd.open_workbook('./人行综合信息系统报价.xlsx')
sheet = xls.sheets()[0]
values = sheet.row_values(2)
print(values)
