from inc.excel_2_json import ReadExcel, WriteJson


# Reading
read_ins = ReadExcel('./data/data_sample.xlsx')

# validation column
read_ins.validation(["INT", "WORD", "BOOL", "STRING", "REAL", "DWORD", "DINT"], 'D_Type')

# rename cols
rename_col = {"Identifier": "identifier","Symbol/Tag - DE": "label_de","Symbol/Tag - EN": "label_en",
              "Source":"source","Address":"address","BitOffset":"bitOffset","DB_Nr":"dataBlockNumber",
              "D_Type":"dataType","Comment":"comment","Label":"label_new","Labels EN":"label_new_en","Selected":"selected", "Comment EN":"comment_en"
              }

read_ins.col_rename(rename_col)

# remove nan
read_ins.rm_nan('identifier')
read_ins.rm_nan('label_de')
read_ins.rm_nan('label_en')


# filter
read_ins.filter_val(['A', 'I', 'M', 'DB'], 'identifier')

# 
write_ins = WriteJson('./results/new_output.json', read_ins.data)
write_ins.refactor()
write_ins.put2file()
