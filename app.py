from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import os
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

#make sure all pre order items are already turn on all the settings
@app.route('/pre-order-open-check') 
def pre_order_open_check():
    driver = webdriver.Chrome(keep_alive=True)
    driver.set_window_size(1100, 800)
    print("Pre Order Open Check starts")
    login_admin(driver)

    os.chdir(path())
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".xls"):
            file_path = f"{file}" 
            df = pd.DataFrame()
            df = pd.read_excel(file_path,index_col=None, header=0)
            df = df.drop(index=0)
            preorder_df = pd.DataFrame()
            preorder_df = df[df['Preorder Product'] == "Y"]

            for sku_id in preorder_df['Product ID (DO NOT EDIT)']:
                click_procedure_open_pre_order(driver, sku_id)
                
    return render_template("index.html", title="open pre order check done")

#make sure all pre order items are already turn on all the settings
@app.route('/pre-order-open-missing-check') 
def pre_order_open_missing_check():
    driver = webdriver.Chrome(keep_alive=True)
    driver.set_window_size(1100, 800)
    print("Pre Order Open Missing Check starts")
    login_admin(driver)

    os.chdir(path())
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".xls"):
            file_path = f"{file}" 
            df = pd.DataFrame()
            df = pd.read_excel(file_path,index_col=None, header=0)
            df = df.drop(index=0)
            ofs_df, preorder_df = pd.DataFrame(), pd.DataFrame()
            preorder_df = df[df['Preorder Product'] == "N"]
            stock_level = preorder_df['Quantity (DO NOT EDIT)']
            ofs_df = preorder_df[stock_level <= 0]

            for sku_id in ofs_df['Product ID (DO NOT EDIT)']:
                msg = click_procedure_missing_pre_order(driver, sku_id)
                print(msg)
                
    return render_template("index.html", title="check pre order done")

#close pre order when there is stock online
@app.route('/close-pre-order')
def pre_order_close():
    driver = webdriver.Chrome(keep_alive=True)
    driver.set_window_size(1100, 800)
    print("Close Pre Order starts")
    login_admin(driver)

    # cross check with stock level
    os.chdir("Check")
    file_path = os.listdir()[0]
    stock_df = pd.read_excel(file_path,index_col=None, header=0)

    os.chdir("..")
    os.chdir(path())
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".xls"):
            file_path = f"{file}" 
            df, havestock_df, preorder_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
            df = pd.read_excel(file_path,index_col=None, header=0)
            df = df.drop(index=0)
            preorder_df = df[df['Preorder Product'] == "Y"]
            havestock_df = preorder_df[preorder_df['Quantity (DO NOT EDIT)'] > 0]
            for barcode in havestock_df["Barcode"]:
                check_stock_df = stock_df.loc[stock_df['商品條碼'] == barcode]
                if int(check_stock_df['預設倉庫']) > 0:
                    tmp_df = pd.DataFrame()
                    tmp_df = df.loc[df['Barcode'] == barcode]
                    if tmp_df.shape[0] > 0:
                        for sku_id in tmp_df['Product ID (DO NOT EDIT)']:
                            click_procedure_close_pre_order(driver, str(sku_id))

    return render_template("index.html", title="close pre order done")

def path():
    excel_folder_location = "Update"
    return excel_folder_location

def login_admin(driver):
    #login admin account
    username = "info@waddystore.com"
    password = "Waddy1208"
    driver.get('https://admin.shoplineapp.com/admin/waddystore/')
    driver.find_element(By.ID, "staff_email").send_keys(username)
    driver.find_element(By.ID, "staff_password").send_keys(password)
    driver.find_element(By.ID, "reg-submit-button").click()
    print("Login sucessful")

def click_procedure_missing_pre_order(driver, sku_id):
    print("Now browsing to SKU: " + sku_id)
    driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
    print("Go to Price and Quantity Tab")
    accept_button = driver.find_element(By.XPATH,'//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input')
    accept_button_classess = accept_button.get_attribute("class")
    if "ng-touched" in accept_button_classess:
        driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
        print("Go to Settings Tab")
        pre_order_switch = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
        pre_order_switch_classess = pre_order_switch.get_attribute("class")
        if "switch-off" in pre_order_switch_classess:
            driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div/span[2]').click()
            print("Switched on Preorder Product Setting")
            
            pre_order_msg_english = "This product is a pre-order product. It will arrive in about 7-14 working days, thank you for your patient! (AVAILABLE does not mean in stock)"
            pre_order_msg_chinese = "此商品為預購商品，大約7-14工作天到貨，請耐心等候♡（尚有庫存不代表有現貨）"
            
            english_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[2]/div/div[2]/div/input')
            english_msg_box.send_keys(Keys.CONTROL, 'a')
            english_msg_box.send_keys(pre_order_msg_english)
            print("Typed in Preorder Product Note (English)")
            chinese_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[3]/div/div[2]/div/input')
            chinese_msg_box.send_keys(Keys.CONTROL, 'a')
            chinese_msg_box.send_keys(pre_order_msg_chinese)
            print("Typed in Preorder Product Note (Chinese)")

            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
            print("Saved changes, completed")
        return " Pre order settings"
    else:
        return "No Missing Pre order settings"

def click_procedure_close_pre_order(driver, sku_id):
    print("Now browsing to SKU: " + sku_id)
    driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
    print("Go to Price and Quantity Tab")
    accept_button = driver.find_element(By.XPATH,'//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input')
    accept_button_classess = accept_button.get_attribute("class")
    if "ng-untouched" in accept_button_classess:
        accept_button.click()
        print("Unticked Accept orders when out of stock")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
    print("Go to Settings Tab")

    pre_order_switch = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
    pre_order_switch_classess = pre_order_switch.get_attribute("class")
    if "switch-on" in pre_order_switch_classess:
        driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div/span[2]').click()
        print("Switched off Preorder Product Setting")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
    print("Saved changes, completed")
    
def click_procedure_open_pre_order(driver, sku_id):
    print("Now browsing to SKU: " + sku_id)
    driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
    print("Go to Price and Quantity Tab")
    accept_button = driver.find_element(By.XPATH,'//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input')
    accept_button_classess = accept_button.get_attribute("class")
    if "ng-untouched" not in accept_button_classess:
        accept_button.click()
    print("Ticked Accept orders when out of stock")
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
    print("Go to Settings")
    pre_order_switch = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
    pre_order_switch_classess = pre_order_switch.get_attribute("class")
    if "switch-off" in pre_order_switch_classess:
        driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div/span[2]').click()
        print("Switched on Preorder Product Setting")
        
    pre_order_msg_english = "This product is a pre-order product. It will arrive in about 7-14 working days, thank you for your patient! (AVAILABLE does not mean in stock)"
    pre_order_msg_chinese = "此商品為預購商品，大約7-14工作天到貨，請耐心等候♡（尚有庫存不代表有現貨）"
    
    english_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[2]/div/div[2]/div/input')
    english_msg_box.send_keys(Keys.CONTROL, 'a')
    english_msg_box.send_keys(pre_order_msg_english)
    print("Typed in Preorder Product Note (English)")
    chinese_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[3]/div/div[2]/div/input')
    chinese_msg_box.send_keys(Keys.CONTROL, 'a')
    chinese_msg_box.send_keys(pre_order_msg_chinese)
    print("Typed in Preorder Product Note (Chinese)")

    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
    print("Saved changes, completed")