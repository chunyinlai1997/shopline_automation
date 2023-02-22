import pandas as pd
import os

class Converter():

    def __init__(self):
        pass
    
    def to_csv(self, data_folder='data/'):
        os.chdir(data_folder)
        for file in os.listdir():
            # Check whether file is in xls format
            if file.endswith(".xls"):
                file_path = f"{file}"
                read_file = pd.read_excel(file_path, engine='xlrd')
                file_name = ''
                if data_folder == "data/updates/":
                    file_name = str(file) + '.csv'
                else:
                    file_name = 'inventory.csv'
                read_file.to_csv(file_name, index=None, header=True)
        os.chdir('../..')

class Reader():

    def __init__(self):
        pass

    def get_df(self, data_folder='data/'):
        os.chdir(data_folder)
        for file in os.listdir():
            if file.endswith(".csv"):
                file_path = f"{file}"
                df = pd.read_csv(file_path, index_col=None, header=0)
                break
        os.chdir('../..')
        return df