from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import pandas as pd
import math
import time

path = "Update"
os.chdir(path)
for file in os.listdir():

    # Check whether file is in text format or not
    if file.endswith(".xls"):
        file_path = f"{file}" 
        df = pd.DataFrame()
        df = pd.read_excel(file_path,index_col=None, header=0)
        df = df.drop(index=0)
        ofs_df, preorder_df = pd.DataFrame(), pd.DataFrame()
        preorder_df = df[df['Preorder Product'] == "N"]
        ofs_df = preorder_df[preorder_df['Quantity (DO NOT EDIT)'] == 0]

        for sku_id in ofs_df['Product Name (English)']:
            print(sku_id)
        print(ofs_df.size)



