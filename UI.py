import streamlit as st
import pandas as pd
import numpy as np
import datetime
from inc.excel_2_json import ReadExcel, WriteJson

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
def process(type, filename):
    if type == 'Excel to Json':
        read_ins = ReadExcel(filename)

        read_ins.validation(["INT", "WORD", "BOOL", "STRING", "REAL", "DWORD", "DINT"], 'D_Type')

        rename_col = {"Identifier": "identifier","Symbol/Tag - DE": "label_de","Symbol/Tag - EN": "label_en",
                    "Source":"source","Address":"address","BitOffset":"bitOffset","DB_Nr":"dataBlockNumber",
                    "D_Type":"dataType","Comment":"comment","Label":"label_new","Labels EN":"label_new_en","Selected":"selected", "Comment EN":"comment_en"
                    }
        read_ins.col_rename(rename_col)

        read_ins.rm_nan('identifier')
        read_ins.rm_nan('label_de')
        read_ins.rm_nan('label_en')

        read_ins.filter_val(['A', 'I', 'M', 'DB'], 'identifier')

        write_ins = WriteJson('./results/excel2json.json', read_ins.data)
        write_ins.refactor()
        write_ins.put2file()

        with open("./results/excel2json.json", "rb") as file:
            now = datetime.datetime.now()
            with download:
                st.download_button(
                    label="Download image",
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

# Stage_2 (select filen)
# download = st.container()
if option != 'Not selected':
    uploaded_file = st.file_uploader("Choose your input file", accept_multiple_files=False, )
    if uploaded_file is not None:
        if option == 'Excel to Json' and not uploaded_file.name.endswith('.xlsx'):
            st.warning('You need select only excel files', icon="⚠️")
        else:
            btn2 = st.button('Start converting', use_container_width = True, type='primary', on_click=process, args=(option,uploaded_file))
            download,_ = st.columns(2)
        
        

            



