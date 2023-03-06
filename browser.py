from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import xlrd
import json
import time

class Action():
    def __init__(self) -> None:
        pass
    
        

    def open_preorder(self, process_list: list):
        driver = webdriver.Chrome(keep_alive=True)
        driver.set_window_size(1100, 800)
        print("Clicker starts")
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
        time.sleep(5)
        
        try:
            driver.find_element(By.ID, "reg-submit-button").click()
            print("Login Shopline Admin successful")
        except NoSuchElementException:
            human = input("Is there a captcha? If done, please type 'ok': ")
            while human.lower() != "ok":
                human = input("Please type 'ok' when done: ")
            print("Login Shopline Admin manually.")

        time.sleep(5)
        
        

    def close_preorder(self, process_list):
        driver = webdriver.Chrome(keep_alive=True)
        driver.set_window_size(1100, 800)
        print("Clicker starts")
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
        time.sleep(5)
        
        try:
            driver.find_element(By.ID, "reg-submit-button").click()
            print("Login Shopline Admin successful")
        except NoSuchElementException:
            human = input("Is there a captcha? If done, please type 'ok': ")
            while human.lower() != "ok":
                human = input("Please type 'ok' when done: ")
            print("Login Shopline Admin manually.")

        time.sleep(5)

        for sku_id, has_varient in process_list:
            print("Now browsing to SKU: " + sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            driver.implicitly_wait(20)
            time.sleep(5)

            if has_varient is False:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                print("Go to Price and Quantity Tab")
                xpath = '//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input'
                if self.pre_order_button_handler(driver,xpath,"close") is False:
                    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                    self.pre_order_button_handler(driver,xpath,"close")

            else:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[5]/a').click()
                print("Go to Variations Tab")
                xpath = '//*[@id="productForm-variations"]/div/div[3]/div[3]/div[1]/div/div/div[2]/div/div[5]/label/input'
                if self.pre_order_button_handler(driver,xpath,"close") is False:
                    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[5]/a').click()
                    self.pre_order_button_handler(driver,xpath,"close")

            element = WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a')))
            element.click()
            print("Go to Settings Tab")

            pre_order_switch = driver.find_element(By.XPATH, '//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
            pre_order_switch_classess = pre_order_switch.get_attribute("class")
            if "switch-on" in pre_order_switch_classess:
                ActionChains(driver).move_to_element(pre_order_switch).click().perform()
                print("Switched off Preorder Product Setting")
            else:
                print("No action, Switch alraedy off")

            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
            print("Saved changes, completed")

    def close_preorder_by_keywords(self):
        driver = webdriver.Chrome()

        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
        time.sleep(5)
        
        try:
            driver.find_element(By.ID, "reg-submit-button").click()
            print("Login Shopline Admin successful")
        except NoSuchElementException:
            human = input("Is there a captcha? If done, please type 'ok': ")
            while human.lower() != "ok":
                human = input("Please type 'ok' when done: ")
            print("Login Shopline Admin manually.")

        time.sleep(5)

        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=1000&scope=preorder')
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)

        product_items = json_data['data']['items']
        print("total items found: " + str( len(product_items)))
        keyword = input("Please input the keywords or exact product Chinese name: ")
        process_list = []

        # Loop through each item in the JSON data and check if the keyword matches any value in the "title_translations" dictionary
        for item in product_items:
            chinese_name = item['title_translations']['zh-hant']
            sku_id = item['id']
            has_varient = False
            print()
            if len(item["variations"]) > 0:
                has_varient = True
            
            if keyword in chinese_name:
                print(chinese_name)
                process_list.append([sku_id, has_varient])

        print("total items execute: " + str( len(process_list)))
        self.close_preorder(process_list) 
        print("Task Complete")

    def find_missing_allow_oversale(self):
        driver = webdriver.Chrome()

        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
        time.sleep(5)
        
        try:
            driver.find_element(By.ID, "reg-submit-button").click()
            print("Login Shopline Admin successful")
        except NoSuchElementException:
            human = input("Is there a captcha? If done, please type 'ok': ")
            while human.lower() != "ok":
                human = input("Please type 'ok' when done: ")
            print("Login Shopline Admin manually.")

        time.sleep(5)

        keyword = input("Please input the keywords or exact product Chinese name: ")
        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=10000&query='+ keyword+'&scope=search')
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)

        product_items = json_data['data']['items']
        print("total items found: " + str( len(product_items)))
        
        process_list = []

        data = self.xls_to_list('search/namelist.xls')
        data.pop(0)
        search_for = dict([[row[0], row[1]] for row in data])

        for item in product_items:
            chinese_name = item['title_translations']['zh-hant']
            sku_id = item['id']
            has_varient = False
            if len(item["variations"]) > 0:
                has_varient = True
            
            if keyword in chinese_name:
                if any(key in chinese_name for key in search_for.keys()):
                    print(chinese_name + " in pre-order keyword list, skip")
                else:
                    print(chinese_name)
                    process_list.append([sku_id, has_varient])

        print("total items execute: " + str( len(process_list)))
        self.close_preorder(process_list) 
        print("Task Complete")
