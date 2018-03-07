import xlsxwriter
from xlrd import open_workbook


def writetoexecl(excelname, sheetname, list):
    wb = xlsxwriter.Workbook(excelname)
    ws = wb.add_worksheet(sheetname)
    row = 0
    for col,data in enumerate(list):
        ws.write_column(row, col, data)
    wb.close()


def appendtoexcel():
    wb = open_workbook('MonitorPOE.xlsx')
    for s in wb.sheets():
        print ('Sheet:',s.name)
        print("Last row", s.nrows)
        row = s.nrows+1
        column = s.ncols+1
        print("Last column",s.ncols)

