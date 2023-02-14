import browser
import inv_dataset
import os
import pandas as pd

class Preorder():

    def __init__(self) -> None:
        pass
    
    def process_update_data (self, inventory_folder_path):
        inventory_files = inv_dataset.Converter()
        inventory_files.to_csv(inventory_folder_path)

        inventory = inv_dataset.Reader()
        inv_df = inventory.get_df(inventory_folder_path)
 
        return inv_df

    def PreOrderClose(self, udpate_folder_path, inventory_folder_path):   
        print(os.getcwd())

        inv_df = self.process_update_data(inventory_folder_path)

        clicker = browser.Action()
        process_list = []
        
        update_files = inv_dataset.Converter()
        update_files.to_csv(udpate_folder_path)

        #Start update procedure
        os.chdir(udpate_folder_path)
        
        #go thru each bulk update form csv
        for file in os.listdir():
            if file.endswith(".csv"):
                #in each bulk update form csv
                file_path = f"{file}"
                df = pd.read_csv(file_path, index_col=None, header=0)
                df = df.drop(index=0)

                df = df.loc[df['Preorder Product'] == "Y"]
                df = df.loc[df['Status'] == "Y"]
                
                for barcode in df['Barcode']:
                    df2 = inv_df.loc[inv_df['商品條碼'] == barcode]
                    df2 = df2.loc[df2['預設倉庫'] > 0]
                    for bar in df2['商品條碼']:
                        sku_id = df[df['Barcode']== bar]['Product ID (DO NOT EDIT)'].item()
                        varient_id = df[df['Barcode']== bar]['Variant ID (DO NOT EDIT)'].item()
                        has_varient = True
                        if pd.isnull(varient_id):
                            has_varient = False
                        process_list.append([sku_id, bar, has_varient])

        os.chdir("../..") 
        print(process_list) 
        clicker.close_preorder(process_list)   
        print("All Completed, End Task.")    


    def PreOrderOpen(self, udpate_folder_path, inventory_folder_path):
        print(os.getcwd())
        
        inv_df = self.process_update_data(inventory_folder_path)

        clicker = browser.Action()

        data = clicker.xls_to_list('search/namelist.xls')
        data.pop(0)
        search_for = dict([[row[0], row[1]] for row in data])

        process_list=[]

        #Start update procedure
        #go thru each bulk update form csv
        os.chdir(udpate_folder_path)

        for file in os.listdir():
            if file.endswith(".csv"):
                #in each bulk update form csv
                file_path = f"{file}"
                update_df = pd.read_csv(file_path, index_col=None, header=0)
                update_df = update_df.drop(index=0)

                period_type = ''

                df = update_df.loc[update_df['Product Name (Traditional Chinese)'].str.contains('|'.join(list(search_for.keys())), na = False)]
                
                df = df.loc[df['Preorder Product'] == "N"]
                df = df.loc[df['Status'] == "Y"]

                discon_tag = 'dis'
                df = df.loc[~df['Product Tag'].str.contains(discon_tag, na=False)]

                discon_tag_manual = 'shortage'
                df = df.loc[~df['Product Tag'].str.contains(discon_tag_manual, na=False)]
                
                for barcode in df['Barcode']:
                    df2 = inv_df.loc[inv_df['商品條碼'] == barcode]
                    df2 = df2.loc[df2['預設倉庫'] <= 0]
                    for bar in df2['商品條碼']:
                        sku_id = df[df['Barcode']== bar]['Product ID (DO NOT EDIT)'].item()
                        varient_id = df[df['Barcode']== bar]['Variant ID (DO NOT EDIT)'].item()
                        chinese_product_name = df[df['Barcode']== bar]['Product Name (Traditional Chinese)'].item()

                        for key in search_for.keys():
                            if key in chinese_product_name:
                                period_type = search_for[key]
                        
                        has_varient = True
                        if pd.isnull(varient_id):
                            has_varient = False
                        
                        process_list.append([sku_id, bar, has_varient, period_type])

        print(process_list) 
        os.chdir("../..") 
        clicker.open_preorder(process_list)   
        print("All Completed, End Task.")    