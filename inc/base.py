'''
This class is used as based reading data class and can be used
for any scaling idea

'''
import pandas as pd
from inc.utils import *
import json
from logging import warn
import warnings
warnings.filterwarnings('ignore')

# Reading Class
class Read():
    # Init function
    def __init__(self) -> None:
        self.data = 0

    # Validation method
    def validation(self, valid_val, col_name):
        signals_types_valid = pd.DataFrame(columns=self.data.columns)

        for index, row in self.data.iterrows():
            if data_type_is_valid(row[col_name], valid_val):
                signals_types_valid = signals_types_valid.append(row) 

        print(f"(INFO) validation has been set on {col_name}")
        self.data = signals_types_valid
    
    # Rename columns method
    def col_rename(self, rename_dict):
        # rename columns for later processing
        self.data = self.data.rename(columns=rename_dict) 
        print(f"(INFO) cols has been renamed")
    
    # Remove Nan rows on specific col name
    def rm_nan(self, col_name):
        self.data = self.data.dropna(subset=[col_name])
        print(f"(INFO) Nan rows has been renamed from {col_name}")

    # Filter based on containing values on specific col name
    def filter_val(self, val, col_name):
        self.data = self.data[self.data[col_name].str.split().apply(set(val).intersection).astype(bool)]
        print(f"(INFO) filter values ({val}) from {col_name}")


class Write():
    def __init__(self, filename) -> None:
        self.filename = filename
        self.results  = 0

    def refactor(self):
        pass

    def write(self):
        pass

    def put2file(self, indent=4):
        with open(self.filename, 'w') as fp:
            json.dump(self.results, fp, indent=indent)
