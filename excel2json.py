from inc.read_excel import ReadExcel



read_ins = ReadExcel('./data/data_sample.xlsx')
valided  = read_ins.validation(["INT", "WORD", "BOOL", "STRING", "REAL", "DWORD", "DINT"], 'D_Type')
print(len(valided))