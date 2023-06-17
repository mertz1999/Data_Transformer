'''
This class is used as based reading data class and can be used
for any scaling idea

'''
import pandas as pd
from inc.utils import *
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

        return signals_types_valid       





