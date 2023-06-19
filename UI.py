import streamlit as st
import pandas as pd
import numpy as np
import datetime
from inc.excel_2_json import ReadExcel, WriteJson
from inc.utils import rename_default_excel

# Config streamlit window
st.set_page_config(
    page_title="Data Transformation",
    page_icon="👋",
    layout="centered"
)

# Set style file
with open("./inc/style.css") as source_css:
    st.markdown(f"<style>{source_css.read()}<style>", unsafe_allow_html=True)

# callback function
def process_excel2json(read_ins, valid_name, valid_values, rename_col, remove_nan_cols, filter_names, filter_values):
    read_ins.validation(valid_values, valid_name[0])

    read_ins.col_rename(rename_col)

    for i in remove_nan_cols:
        read_ins.rm_nan(i)

    read_ins.filter_val(filter_values, filter_names[0])

    write_ins = WriteJson('./results/excel2json.json', read_ins.data)

    write_ins.refactor(identifier_label=rename_col["Identifier"],
                       label_label=rename_col["Symbol/Tag - EN"],
                       source_label=rename_col["Source"],
                       address_label=rename_col["Address"],
                       data_type_label=rename_col["D_Type"],
                       comment_label=rename_col["Comment EN"],
                       dataBlockNumber=rename_col["DB_Nr"],
                       bitOffset=rename_col["BitOffset"],
                       )
    write_ins.put2file()

    with open("./results/excel2json.json", "rb") as file:
        now = datetime.datetime.now()
        with download:
            st.download_button(
                label="Download json",
                data=file,
                file_name=f"excel2json_{now.year}_{now.month}_{now.day}__{now.hour}_{now.minute}_{now.second}.json",
            )
            


# header
st.header("Data Transformation Panel")

# Stage_1 (select type of transformation)
option = st.selectbox(
    'Select type of transormation based on your input file and your target?',
    ('Not selected','Excel to Json')
)

if option == 'Excel to Json':
    uploaded_file = st.file_uploader("Choose your input file", accept_multiple_files=False, )
    if uploaded_file is not None:
        if option == 'Excel to Json' and not uploaded_file.name.endswith('.xlsx'):
            st.warning('You need select only excel files', icon="⚠️")

        # Read Data
        read_ins = ReadExcel(uploaded_file)

        # Col filter
        st.subheader('column validation:')
        valid_cols = st.columns(3)
        valid_name  = valid_cols[0].multiselect('validation on which column:',read_ins.data.columns,['D_Type'], max_selections=1)
        valid_values = valid_cols[1].text_input('validation values', 'INT WORD BOOL STRING REAL DWORD DINT')
        valid_values = valid_values.split(' ')

        # Cols rename part
        st.subheader('Rename cols')
        re_cols = st.columns(4)
        rename_input = []
        for idx, col_name in enumerate(list(read_ins.data.columns)):
            select_cols = idx % 4
            rename_input.append(re_cols[select_cols].text_input(str(col_name), rename_default_excel[str(col_name)]))

        rename_col = {read_ins.data.columns[idx]:rename_input[idx] for idx in range(len(rename_input))}

        # remove nan from cols
        st.subheader('Remove Nan from cols:')
        rm_cols = st.columns(4)
        remove_nan = []
        for idx, col_name in enumerate(list(read_ins.data.columns)):
            col_name = rename_col[str(col_name)]
            select_cols = idx % 4
            remove_nan.append(rm_cols[select_cols].checkbox(str(col_name)))

        remove_nan_cols = [rename_col[read_ins.data.columns[idx]] for idx,i in enumerate(remove_nan) if i]

        # Col filter
        st.subheader('Filter specific col')
        filter_cols = st.columns(3)
        filter_names  = filter_cols[0].multiselect('which column you need to filter:',rename_input,rename_col['Identifier'], max_selections=1)
        filter_values = filter_cols[1].text_input('Filtring values:', 'A I M DB')
        filter_values = filter_values.split(' ')

        process_args = (read_ins, valid_name, valid_values, rename_col, remove_nan_cols, filter_names, filter_values)
        btn2 = st.button('Start converting', use_container_width = True, type='primary', on_click=process_excel2json, args=process_args)
        download,_ = st.columns(2)
        
        

            



