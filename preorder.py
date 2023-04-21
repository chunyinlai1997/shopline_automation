from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import json
import time
import xlrd
import logging

class Preorder():

    def __init__(self) -> None:
        pass

    def shopline_login(self, driver):
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)

        wait = WebDriverWait(driver, 120)

        while True:
            try:
                time.sleep(2)
                submit_btn = driver.find_element(By.XPATH, '//*[@id="reg-submit-button"]')
                submit_btn.click()
            except:
                logging.debug("Unable to logged in automatically, blocked by Captcha")
                print("Unable to logged in automatically.")

            # Check if the element is already loaded
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div/react-app')))
                print("Successfully logged in to Shopline.")
                break
            except:
                pass
            
            # Ask the user if there is a captcha
            human = input("Is there a captcha? If done, please type 'ok': ")
            while human.lower() != "ok":
                logging.debug("there is still blocking or captcha issue")
                human = input("Please type 'ok' when done: ")
            
            # Wait for the new page to load
            wait.until(EC.staleness_of(driver.find_element_by_tag_name('html')))
        
    def xls_to_list(self, path):
        workbook = xlrd.open_workbook(path)
        worksheet = workbook.sheet_by_index(0)
        num_rows = worksheet.nrows
        num_cols = worksheet.ncols
        data = []

        for row_idx in range(num_rows):
            row_data = []
            for col_idx in range(num_cols):
                cell_value = worksheet.cell_value(row_idx, col_idx)
                row_data.append(cell_value)
            data.append(row_data)    

        return data

    def period_type_handler(self, period_type):
        words = self.xls_to_list('template/period_template.xls')
        words.pop(0)
        chinese = ''
        english = ''

        if period_type == "A":
            chinese, english = words[0][1], words[0][2]
        elif period_type == "B":
            chinese, english = words[1][1], words[1][2]
        elif period_type == "C":
            chinese, english = words[2][1], words[2][2]
        elif period_type == "D":
            chinese, english = words[3][1], words[3][2]
        elif period_type == "E":
            chinese, english = words[4][1], words[4][2]
        elif period_type == "NA":
            chinese, english = words[5][1], words[5][2]
        else:
            print("type not found")
            logging.error("type not found")
        return chinese, english

    def pre_order_button_handler(self, driver, button_path, mode):
        print("Clicking button or checkbox...")
        button_found = False
        while button_found is False:
            try:
                accept_button = driver.find_element(By.XPATH, button_path)
                button_found = True
            except NoSuchElementException:
                logging.error("NoSuchElementException")
                print("NoSuchElementException")
                button_found = False

        accept_button_status = accept_button.get_attribute('checked')
        print("Checkbox Status is ",accept_button_status)

        if mode == "open":
            if accept_button_status == True or accept_button_status == "true":
                print("pass clicking checkbox, already checked")
            elif accept_button_status == None:
                print("clicking checkbox")
                try:
                    driver.find_element(By.XPATH,button_path).click()
                except ElementNotInteractableException:
                    logging.error("ElementNotInteractableException")
                    print("ElementNotInteractableException")
                    return False
                except NoSuchElementException:
                    logging.error("NoSuchElementException")
                    print("NoSuchElementException")
                    return False
            else:
                logging.error("fall into else, cannot locate button")
                pass
        elif mode == "close":
            if accept_button_status == True or accept_button_status == "true":
                print("clicking checkbox")
                try:
                    driver.find_element(By.XPATH,button_path).click()
                except ElementNotInteractableException:
                    logging.error("ElementNotInteractableException")
                    print("ElementNotInteractableException")
                    return False
                except NoSuchElementException:
                    logging.error("NoSuchElementException")
                    print("NoSuchElementException")
                    return False              
            elif accept_button_status == None:
                print("pass clicking checkbox, already unchecked")
            else:
                logging.error("fall into else, cannot locate button")
                pass
        return True

    def PreOrderCloseAction(self, process_list, driver):
        for sku_id, has_varient in process_list:
            print("Now browsing to SKU: " + sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            driver.implicitly_wait(20)
            time.sleep(5)

            if has_varient is False:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                print("Go to Price and Quantity Tab")
                xpath = '//input[@name="product_out_of_stock_orderable"]'
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

    def PreOrderClose(self):
        driver = webdriver.Chrome()
        process_list = []

        self.shopline_login(driver)
        
        time.sleep(5)

        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=1000&scope=preorder')
        
        time.sleep(5)

        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)
        print("Collected data....")

        product_items = json_data['data']['items']
        print("total items found: " + str(len(product_items)))
        
        for item in product_items:
            quantity = item['quantity']
            status = item['status']
            is_preorder = item['is_preorder']
            sku_id = item['id']
            chinese_name = item['title_translations']['zh-hant']
            has_varient = False
            if len(item["variations"]) > 0:
                has_varient = True

            if int(quantity) > 0 and status == "active" and is_preorder == True:
                print(chinese_name)
                logging.info(chinese_name)
                process_list.append([sku_id, has_varient])
        
        print("Process items: ")
        print(process_list) 
        logging.info("process_list as following")
        logging.info(process_list)
        print("total items to execute: " + str(len(process_list)))
        self.PreOrderCloseAction(process_list, driver)

        print("All Completed, End Task.")

    def PreOrderOpenAction(self, process_list, driver):
        for sku_id, has_varient, period_type in process_list:
            print("Now browsing to SKU: " + sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            driver.implicitly_wait(20)
            if has_varient is False:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                print("Go to Price and Quantity Tab")
                xpath = '//input[@name="product_out_of_stock_orderable"]'
                self.pre_order_button_handler(driver,xpath,"open")
                if self.pre_order_button_handler(driver,xpath,"open") is False:
                    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                    self.pre_order_button_handler(driver,xpath,"open")
            else:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[5]/a').click()
                print("Go to Variations Tab")
                xpath = '//*[@id="productForm-variations"]/div/div[3]/div[3]/div[1]/div/div/div[2]/div/div[5]/label/input'
                if self.pre_order_button_handler(driver,xpath,"open") is False:
                    driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[5]/a').click()
                    self.pre_order_button_handler(driver,xpath,"open")

            element = WebDriverWait(driver, 90).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a')))
            element.click()
            print("Go to Settings Tab")
            pre_order_switch = driver.find_element(By.XPATH, '//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
            pre_order_switch_classess = pre_order_switch.get_attribute("class")
            if "switch-off" in pre_order_switch_classess:
                print("Not yet switched on Preorder Product Setting")
                ActionChains(driver).move_to_element(pre_order_switch).click().perform()
                print("Switched on Preorder Product Setting")

                pre_order_msg_chinese, pre_order_msg_english = self.period_type_handler(period_type) 
                english_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[2]/div/div[2]/div/input')
                english_msg_box.send_keys(Keys.CONTROL, 'a')
                english_msg_box.clear()
                english_msg_box.send_keys(pre_order_msg_english)
                print("Typed in Preorder Product Note (English)")
                chinese_msg_box = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[3]/div/div[2]/div/input')
                chinese_msg_box.send_keys(Keys.CONTROL, 'a')
                chinese_msg_box.clear()
                chinese_msg_box.send_keys(pre_order_msg_chinese)
                print("Typed in Preorder Product Note (Chinese)")   
            elif "switch-on" in pre_order_switch_classess:
                print("Already switched on Preorder Product Setting")
            else:
                print("ERROR, switch not found")

            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
            print("Saved changes, completed")

    def PreOrderOpen(self):
        driver = webdriver.Chrome()
        process_list = []

        self.shopline_login(driver)

        data = self.xls_to_list('search/namelist.xls')
        data.pop(0)
        search_for = dict([[row[0], row[1]] for row in data])

        exclude_list = self.xls_to_list('search/exclude.xls')
        exclude_list.pop(0)

        print("Your exclude list:")
        print(exclude_list)
        print("You may edit under 'search/namelist.xls'")
        print("items found: ")
        
        time.sleep(3)

        for key in search_for.keys():
            time.sleep(0.5)
            driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=10000&query='+ key +'&scope=search')
            html_response = driver.find_element(By.XPATH, '/html/body/pre').text
            json_data = json.loads(html_response)

            product_items = json_data['data']['items']

            for item in product_items:
                quantity = item['quantity']
                status = item['status']
                is_preorder = item['is_preorder']
                sku_id = item['id']
                chinese_name = item['title_translations']['zh-hant']
                has_varient = False
                if len(item["variations"]) > 0:
                    has_varient = True

                not_dis = False

                if item['tags_array'] is None:
                    not_dis = True
                elif 'dis' not in item['tags_array'] or 'dis' not in item['sku']:
                    not_dis = True
                
                if not_dis == True and chinese_name not in exclude_list:
                    if quantity <= 0 and not is_preorder and status == "active":
                        print(chinese_name)
                        logging.info(chinese_name)
                        process_list.append([sku_id, has_varient, search_for[key]])

        print("Collected data....")
        print("Process items: ")
        print(process_list) 
        logging.info("process_list as following")
        logging.info(process_list)
        print("total items to execute: " + str(len(process_list)))

        self.PreOrderOpenAction(process_list, driver)
        
        print("All Completed, End Task.")

    def PreOrderCloseKeywords(self):
        driver = webdriver.Chrome()
        
        self.shopline_login(driver)

        time.sleep(5)

        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=1000&scope=preorder')
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)

        product_items = json_data['data']['items']
        print("total items found: " + str( len(product_items)))
        keyword = input("Please input the keywords or exact product Chinese name: ")
        logging.info('Submitted keyword: ' + keyword)
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

        print("Process items: ")
        print(process_list) 
        print("total items to execute: " + str(len(process_list)))
        logging.info("process_list as following")
        logging.info(process_list)

        self.PreOrderCloseAction(process_list, driver)
        print("Task Complete")

    def FindMissingPreOrderOpen(self):
            driver = webdriver.Chrome()
            
            self.shopline_login(driver)

            time.sleep(5)

            keyword = input("Please input the keywords or exact product Chinese name: ")

            driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?page=1&offset=0&limit=10000&query='+ keyword+'&scope=search')
            html_response = driver.find_element(By.XPATH, '/html/body/pre').text
            json_data = json.loads(html_response)

            product_items = json_data['data']['items']
            print("total items found: " + str(len(product_items)))
            
            process_list = []

            data = self.xls_to_list('search/namelist.xls')
            data.pop(0)
            search_for = dict([[row[0], row[1]] for row in data])

            for item in product_items:
                chinese_name = item['title_translations']['zh-hant']
                sku_id = item['id']
                quantity = item['quantity']
                has_varient = False
                if quantity > 0: 
                    pass
                else:
                    if len(item["variations"]) > 0:
                        has_varient = True

                    if keyword in chinese_name:
                        if any(key in chinese_name for key in search_for.keys()):
                            print(chinese_name + " in pre-order keyword list, skip")
                            logging.info(chinese_name + " in pre-order keyword list, skip")
                        else:
                            print(chinese_name)
                            logging.info(chinese_name)
                            process_list.append([sku_id, has_varient, 'C'])

            print("Process items: ")
            print(process_list) 
            print("total items to execute: " + str(len(process_list)))
            logging.info("process_list as following")
            logging.info(process_list)
            
            self.PreOrderOpenAction(process_list, driver)
            print("Task Complete")
