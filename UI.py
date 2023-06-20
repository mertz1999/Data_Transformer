import streamlit as st
import pandas as pd
import numpy as np
import datetime
from inc.data_methods import DataMethods
from inc.output_methods import OutputMethods
import json

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
def process_excel2json(dataframe,output_config):
    out_ins = OutputMethods(dataframe)
    output = out_ins.itrate_and_apply_json(output_config)
    with open('./results/excel2json.json', 'w') as fp:
        json.dump(output, fp, indent=4)


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
    # Get Uploaded files
    data_file     = st.file_uploader("Choose your input file", accept_multiple_files=False, )
    input_config  = st.file_uploader("Choose your input config file", accept_multiple_files=False, )
    output_config = st.file_uploader("Choose your output config file", accept_multiple_files=False, )

    # Check uploaded files
    if (data_file is not None) and (input_config is not None) and (output_config is not None):
        if option == 'Excel to Json' and not data_file.name.endswith('.xlsx'):
            st.warning('You need select only excel files', icon="⚠️")

        # write files temporary
        with open('./configs/temp1.json', 'wb') as f: f.write(input_config.read())
        with open('./configs/temp2.json', 'wb') as f: f.write(output_config.read())

        # Load excel file
        data = pd.read_excel(data_file)
        method_instance = DataMethods(data)
        method_instance.apply_json('./configs/temp1.json')


        btn2 = st.button('Start converting', use_container_width = True, type='primary', on_click=process_excel2json, args=(method_instance.dataframe, './configs/temp2.json'))
        download,_ = st.columns(2)
        
        

            



