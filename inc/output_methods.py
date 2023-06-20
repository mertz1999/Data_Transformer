import pandas as pd
import json
import re

class OutputMethods():
    def __init__(self, dataframe=pd.DataFrame({''})) -> None:
        self.dataframe = dataframe
    
    # Check if input has # in first char (use for add col value)
    def hash_check(self, input, row):
        if input != "" and input[0] == "#":
            return row[input[1:]]
        else:
            return False
    
    # Check if input has # in first char (use for call a method)
    def at_check(self, input, row):
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
        results = []
        for i, row in self.dataframe.iterrows():
            results.append(self.apply_json(jsonfile, row))
        
        return results
