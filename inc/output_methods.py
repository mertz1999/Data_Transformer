"""
This file contain OutputMethods that will perform on dataframe and make your desired output for example make a json file based
on your instrunction that is save in .json config file.
"""
import pandas as pd
import json
import re

class OutputMethods():
    '''
    This method is contain all method that need to apply on dataframes row for saving on output file
    * Methods:
        1. hash_check: if in json config file you write #col_name this method will get col_name value of a row
        2. at_check: if in json config file you write @method_name this method will run method_name and pass all :#col_name
        to method_name (ex. "@dataClass_mapping:#dataType"  in this instrunction dataClass_mapping will be run and pass dataType
        value of row to this method)
    '''
    def __init__(self, dataframe) -> None:
        '''
        * inputs: pass dataframe to this class inintializaition
        '''
        self.dataframe = dataframe
    
    # Check if input has # in first char (use for add col value)
    def hash_check(self, input, row):
        """
        This method get input like @col_name and select col_name value from input row
        """
        if input != "" and input[0] == "#":
            return row[input[1:]]
        else:
            return False
    
    # Check if input has # in first char (use for call a method)
    def at_check(self, input, row):
        '''
        This function check which method you select to running (@method_name) and get col_name that is
        used like this:   ':#col_name1:#colname2'
        '''
        if input != "" and input[0] == "@":
            args = input[1:].split(':#')
            if args[0] == "dataClass_mapping":
                return self.dataClass_mapping(args[1], row)
            elif args[0] == "source_mapping":
                return self.source_mapping(args[1:], row)
            elif args[0] == "dataType_mapping":
                return self.dataType_mapping(args[1:], row)
        else:
            return False
    
    # mapping method for dataclass
    def dataClass_mapping(self,arg, row):
        '''
        This method is used based on your notebook
        '''
        if row[arg] == "BOOL":
            return "digital"
        elif row[arg] in ["REAL"]:
            return "analog"
        elif row[arg] in ["INT", "DINT", "WORD", "DWORD"]:
            return "discrete"
        elif row[arg] == "STRING":
            return "string"
        else:
            return "NOT FOUND"
    
    # mapping method for source
    def source_mapping(self,arg, row):
        '''
        This method is used based on your notebook
        '''
        if 'DB' in row[arg[0]]:
            return {
                "name": "datablock",
                "dataBlockNumber": row[arg[1]],
                "address": int(row[arg[2]])
            }
        elif row[arg[0]] == 'A':
            return {
                "name": "output",
                "address": int(row[arg[2]])
            }
        elif row[arg[0]] == 'M':
            return {
                "name": "memory",
                "address": int(row[arg[2]])
            }
        elif row[arg[0]] == 'I':
            return {
                "name": "input",
                "address": int(row[arg[2]])
            }
    
    # mapping method for dataType
    def dataType_mapping(self,arg, row):
        '''
        This method is used based on your notebook
        '''
        # definition of the config.dataType in the json
        if '[' in row[arg[0]] and ']' in row[arg[0]]:
            byte_count = int(re.findall(r'\d+', row[arg[0]])[0])
            row[arg[0]] = 'string'
        else:
            byte_count = None

        if byte_count is not None:
            return {
                "name": row[arg[0]],
                "byteCount": byte_count
            }
        else:
            if not pd.isna(row[arg[1]]):
                return {
                    "name"      : row[arg[0]],
                    "bitOffset" : int(row[arg[1]])
                }
            else: 
                return {
                    "name": row[arg[0]]
                }


    # Apply Json config file
    def apply_json(self, jsonfile, row):
        '''
        This method will read data from json config file and check @,# and pass them to hash_check and at_check methods
        This method is a little confusing.
        '''
        # Load json file
        with open(jsonfile, 'r') as f:
            configs = json.load(f)

            # Check which method is used and apply it
            for key in configs.keys():
                if type(configs[key]) == str:
                    temp = self.hash_check(configs[key], row)
                    if temp: configs[key] = temp  

                elif type(configs[key]) == dict:
                    for key2 in configs[key].keys():                            
                        temp = self.hash_check(configs[key][key2], row)
                        if temp :
                            configs[key][key2] = temp
                            continue

                        # check if has @
                        temp = self.at_check(configs[key][key2], row)
                        if temp : 
                            configs[key][key2] = temp
                            continue


            return configs

    def itrate_and_apply_json(self, jsonfile):
        '''
        with this method we will itrate on all rows and make dictionary for saving baed on your instruction on 
        .json config file.
        '''
        results = []
        for i, row in self.dataframe.iterrows():
            results.append(self.apply_json(jsonfile, row))
        
        return results
