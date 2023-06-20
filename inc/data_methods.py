'''
This class is used for all method that you need to apply on each pandas
dataframe

'''
import pandas as pd
from inc.utils import *
import json
import warnings
warnings.filterwarnings('ignore')


class DataMethods():
    def __init__(self, dataframe=pd.DataFrame({''})) -> None:
        self.dataframe = dataframe
    
    # Validation method
    def validation(self, valid_val, col_name):
        signals_types_valid = pd.DataFrame(columns=self.dataframe.columns)

        for index, row in self.dataframe.iterrows():
            if data_type_is_valid(row[col_name], valid_val):
                signals_types_valid = signals_types_valid.append(row) 

        self.dataframe = signals_types_valid

    # Rename columns method
    def renaming(self, rename_dict):
        # rename columns for later processing
        self.dataframe = self.dataframe.rename(columns=rename_dict) 

    # Remove Nan rows on specific col name
    def remove_nan(self, col_name):
        self.dataframe = self.dataframe.dropna(subset=[col_name])

    # Filter based on containing values on specific col name
    def filtering(self, val, col_name):
        self.dataframe = self.dataframe[self.dataframe[col_name].str.split().apply(set(val).intersection).astype(bool)]

    # Apply Json config file
    def apply_json(self, jsonfile):
        # Load json file
        with open(jsonfile, 'r') as f:
            configs = json.load(f)

            # Check which method is used and apply it
            for method_name in configs.keys():
                # apply validation method
                if method_name[1:] == 'validation':
                    for args in configs[method_name]: self.validation(args["values"],args["col_name"])

                # apply renaming method
                elif method_name[1:] == 'renaming':
                    self.renaming(configs[method_name])
                
                # apply remove nan mathod
                elif method_name[1:] == 'remove_nan':
                    for args in configs[method_name]: self.remove_nan(args)

                # apply filtering
                elif method_name[1:] == 'filtering':
                    for args in configs[method_name]: self.filtering(args["values"],args["col_name"])
                
                
                    

            
