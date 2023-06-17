from inc.base import Read
import pandas as pd


class ReadExcel(Read):
    def __init__(self, file_path) -> None:
        super().__init__()

        # Reading Data
        self.data = pd.read_excel(file_path)
        print("(INFO) Data has been readed sucsessfully as pandas dataframe!")

