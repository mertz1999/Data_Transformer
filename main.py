from inc.data_methods import DataMethods
from inc.output_methods import OutputMethods
import pandas as pd
import json

# Reading data
data = pd.read_excel("./data/data_sample.xlsx")

# load input json file and apply different methods
method_instance = DataMethods(data)
method_instance.apply_json('./configs/input_config.json')

# Load output json file 
out_ins = OutputMethods(method_instance.dataframe)
output = out_ins.itrate_and_apply_json('./configs/output_config.json')

# save results
with open('./temp.json', 'w') as fp:
    json.dump(output, fp, indent=4)
