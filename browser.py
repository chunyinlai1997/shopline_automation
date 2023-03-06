from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import preorder

class Action():
    def __init__(self) -> None:
        pass

    def close_preorder_by_keywords(self):
        driver = webdriver.Chrome()
        func = preorder.Preorder()
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
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
        func.PreOrderCloseAction(process_list, driver)
        print("Task Complete")

    def find_missing_allow_oversale(self):
        driver = webdriver.Chrome()
        func = preorder.Preorder()
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        
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
        func.PreOrderOpenAction(process_list, driver)
        print("Task Complete")
