'''
Base Input of this class is a pandas dataframe after reading data so
you can use this class for every input file that you convert it to 
a pandas dataframe.

'''
import pandas as pd
# from inc.utils import *
import json
import warnings
warnings.filterwarnings('ignore')

class DataMethods():
    '''
    ##### working with pandas dataframe:
        Input: your dataframe
        mehtods:
            1. validation: for check a col_name is equal to some values or not
            2. renaming: rename column names
            3. remove_nan: remove Nan value from epecific column
            4. filtering: for check a col_name is contained some values or not
            5. apply_json: reading json config file a check which method will be applyed on dataframe

    '''
    def __init__(self, dataframe) -> None:
        '''
        ##### Initialization method and get dataframe
        '''
        self.dataframe = dataframe        
    
    # Validation method
    def validation(self, valid_val, col_name):
        '''
        ##### check a col_name is equal to some values or not
            Inputs:
                1. valid_val: a list if values that you want to check (ex. ["INT", "WORD", "BOOL", "STRING", "REAL", "DWORD", "DINT"])
                2. col_name: on which column name you need to apply these values
        '''
        signals_types_valid = pd.DataFrame(columns=self.dataframe.columns)

        for index, row in self.dataframe.iterrows():
            if data_type_is_valid(row[col_name], valid_val):
                signals_types_valid = signals_types_valid.append(row) 

        self.dataframe = signals_types_valid

    # Rename columns method
    def renaming(self, rename_dict):
        '''
        ##### rename columns of dataframe
            inputs: 
                1. rename_dict: you need to pass a dictionary that contain your new name:
        '''
        # rename columns for later processing
        self.dataframe = self.dataframe.rename(columns=rename_dict) 

    # Remove Nan rows on specific col name
    def remove_nan(self, col_name):
        '''
        ##### remove any nan rows on a column
            inputs:
                1. col_name: which column do you need to be checking
        '''
        self.dataframe = self.dataframe.dropna(subset=[col_name])

    # Filter based on containing values on specific col name
    def filtering(self, val, col_name):
        '''
        ##### filter rows on a column that contain one of the values
            inputs:
                1. val: a list of values
                2. col_name: selected column
        '''
        self.dataframe = self.dataframe[self.dataframe[col_name].str.split().apply(set(val).intersection).astype(bool)]

    # Apply Json config file
    def apply_json(self, jsonfile):
        '''
        ##### The important part of this class that read input config (json) file and then after parsing, it will apply the instructions.
        
            inputs:
                1. jsonfile: your json filename

        in config file use @ for select which method you need to select as key value in json file and values 
        can be pass as a list but it contail different values that depends on the method.

        '''
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
                
                
                    

            


def data_type_is_valid(type: str, DATA_TYPES_VALID):
    if type.startswith("STRING"):
        return True
    if type in DATA_TYPES_VALID:
        return True
    return False