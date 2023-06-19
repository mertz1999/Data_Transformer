from inc.base import Read, Write
import pandas as pd
import re

class ReadExcel(Read):
    def __init__(self, file_path) -> None:
        super().__init__()

        # Reading Data
        self.data = pd.read_excel(file_path)
        print("(INFO) Data has been readed sucsessfully as pandas dataframe!")

class WriteJson(Write):
    def __init__(self, filename, data) -> None:
        super().__init__(filename)
        self.data = data
    
    def refactor(self, 
                 identifier_label = 'identifier',
                 label_label='label_en',
                 source_label='source',
                 address_label='address',
                 data_type_label='dataType',
                 comment_label='comment_en',
                 dataBlockNumber='dataBlockNumber',
                 bitOffset = 'bitOffset'                 
                 ):
        self.results = []
        for i, row in self.data.iterrows():
            # definition of fields within the final json
            identifier = row[identifier_label]
            label = row[label_label]
            source = row[source_label]
            address = row[address_label]
            data_type = row[data_type_label]
            comment = str(row[comment_label])
            unit = ""
            scaling_factor = 1
            scaling_offset = 0
            enabled = False
            

            # mapping of S7 datatype to standard datatype
            if data_type == "BOOL":
                dataType = "boolean"
            elif data_type == "REAL":
                dataType = "real"
            elif data_type == "INT":
                dataType = "int16"
            elif data_type == "DINT":
                dataType = "int32"
            elif data_type == "WORD":
                dataType = "word"
            elif data_type == "DWORD":
                dataType = "dword"
            elif data_type == "STRING":
                dataType = "string"

            # definition of the first level of the json
            out_dict = {
                "enabled": enabled,
                "label": label,
                "unit": unit,
                "scalingFactor": scaling_factor,
                "scalingOffset": scaling_offset,
                "config": {}
            }

            # definition of second level fields in the config in the json
            out_dict["config"]["identifier"] = identifier
            out_dict["config"]["comment"] = comment

            # definition of the config.dataClass in the json
            if data_type == "BOOL":
                out_dict["config"]["dataClass"] = "digital"
            elif data_type in ["REAL"]:
                out_dict["config"]["dataClass"] = "analog"
            elif data_type in ["INT", "DINT", "WORD", "DWORD"]:
                out_dict["config"]["dataClass"] = "discrete"
            elif data_type == "STRING":
                out_dict["config"]["dataClass"] = "string"

            # definition of the config.source in the json
            if 'DB' in source:
                out_dict["config"]["source"] = {
                    "name": "datablock",
                    dataBlockNumber: row[dataBlockNumber],
                    "address": int(address)
                }
            elif source == 'A':
                out_dict["config"]["source"] = {
                    "name": "output",
                    "address": int(address)
                }
            elif source == 'M':
                out_dict["config"]["source"] = {
                    "name": "memory",
                    "address": int(address)
                }
            elif source == 'I':
                out_dict["config"]["source"] = {
                    "name": "input",
                    "address": int(address)
                }
            
            # definition of the config.dataType in the json
            if '[' in data_type and ']' in data_type:
                byte_count = int(re.findall(r'\d+', data_type)[0])
                data_type = 'string'
            else:
                byte_count = None

            if byte_count is not None:
                out_dict["config"]["dataType"] = {
                    "name": dataType,
                    "byteCount": byte_count
                }
            else:
                if not pd.isna(row[bitOffset]):
                    out_dict["config"]["dataType"] = {
                        "name": dataType,
                         bitOffset: int(row[bitOffset])
                    }
                else: 
                    out_dict["config"]["dataType"] = {
                        "name": dataType
                    }

            # output from transformation
            self.results.append(out_dict)
