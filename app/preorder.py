from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import shopline_login_handler as ShoplineLogin
import driver as Driver
import json
import time
import xlrd
import logging
import requests

class Preorder():

    def __init__(self, config_path='config.json') -> None:
        self.login_handler = ShoplineLogin.ShoplineLoginHandler()
        self.config_path = config_path
        self.webdriver = Driver.WebDriver()

    def read_config(self) -> json:
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    
    def config_url(self) -> str:
        config = self.read_config()
        return config["login_url"]
    
    def api_url(self) -> str:
        config = self.read_config()
        return config["api_url"]
    
    def shopline_login(self, driver) -> None:
        self.login_handler.shopline_login(driver)

    def xls_to_list(self, path) -> list:
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
    
    def xpath_selector(self, sub_type, key) -> str:
        config = self.read_config()
        try:
            return config["xpath"][sub_type][key]
        except:
            msg = "No Corresponding Xpath in configuration."
            print(msg)
            logging.error(msg)
            return ""
    
    def tab_click_handler(self, driver, by, selector, max_attempts=15, delay=1) -> bool:
        for attempt in range(max_attempts):
            try:
                element = driver.find_element(by, selector)
                element.click()
                return True  # Click succeeded
            except (ElementNotInteractableException, ElementClickInterceptedException):
                msg = f"Attempt {attempt + 1}: Click failed, retrying..."
                print(msg)
                logging.debug(msg)
                time.sleep(delay)
        return False  # Click failed after max_attempts

    def tab_click(self, driver, key):
        selector = self.xpath_selector("tab", key)
        if self.tab_click_handler(driver, By.XPATH, selector):
                print("Go to " + key +" tab")
        else:
            print("Unable to go " + key +" Tab, skip")

    def switch_click_handler(self, driver, element, max_attempts=3, delay=1) -> bool:
        for attempt in range(max_attempts):
            try:
                action = ActionChains(driver)
                action.move_to_element(element).click().perform()
                return True  # Click succeeded
            except (ElementNotInteractableException, ElementClickInterceptedException):
                print(f"Attempt {attempt + 1}: Click failed, retrying...")
                time.sleep(delay)
        return False  # Click failed after max_attempts

    def period_type_handler(self, period_type) -> (str, str):
        words = self.xls_to_list('template/period_template.xls')
        words.pop(0)
        
        type_mapping = {
            "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "NA": 5
        }

        try:
            index = type_mapping[period_type]
            chinese, english = words[index][1], words[index][2]
        except KeyError:
            msg = "Type not found"
            print(msg)
            logging.error(msg)
            raise ValueError("Type not found")

        return chinese, english
    
    def checkbox_click(self, driver, button_path) -> bool:
        print("clicking checkbox")
        try:
            driver.find_element(By.XPATH, button_path).click()
            return True
        except (ElementNotInteractableException, NoSuchElementException):
            msg = "unable to click the checkbox"
            logging.debug(msg)
            print(msg)
            return False

    def pre_order_button_handler(self, driver, button_path, mode) -> bool:
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
        print("Checkbox Status is ", accept_button_status)

        if mode == "open":
            if accept_button_status == True or accept_button_status == "true":
                print("pass clicking checkbox, already checked")
            elif accept_button_status == None:
                if self.checkbox_click(driver, button_path):
                    return False
            else:
                logging.error("fall into else, cannot locate button")
                pass
        elif mode == "close":
            if accept_button_status == True or accept_button_status == "true":
                if self.checkbox_click(driver, button_path):
                    return False
            elif accept_button_status == None:
                print("pass clicking checkbox, already unchecked")
            else:
                logging.error("unable to locate button")
                pass
        return True

    def pre_order_click(self, driver, key, xpath, option) -> None:
        if self.pre_order_button_handler(driver,xpath, option) is False:
            msg = "pre order button failed, retrying..."
            print(msg)
            logging.debug(msg)
            self.tab_click(driver, key)
            self.pre_order_button_handler(driver,xpath, option)
        else:
            pass

    def pre_order_switch_off_handler(self, driver) -> None:
        pre_order_switch_xpath = self.xpath_selector("Setting_tab", "pre_order_switch")
        pre_order_switch = driver.find_element(By.XPATH, pre_order_switch_xpath)
        pre_order_switch_classess = pre_order_switch.get_attribute("class")

        if "switch-on" in pre_order_switch_classess:
            if self.switch_click_handler(driver, pre_order_switch):
                print("Switch clicked successfully.")
            else:
                print("Switch click failed after multiple attempts.")
            print("Switched off Preorder Product Setting")
        else:
            print("No action, Switch alraedy off")

    def pre_order_switch_on_handler(self, driver, period_type, replace) -> None:
        pre_order_switch_xpath = self.xpath_selector("Setting_tab", "pre_order_switch")
        pre_order_switch = driver.find_element(By.XPATH, pre_order_switch_xpath)
        pre_order_switch_class = pre_order_switch.get_attribute("class")
        
        def type_in_msg_box(driver, msg_box, message, max_attempts=8, delay=1):
            for attempt in range(max_attempts):
                try:
                    msg_box.send_keys(Keys.CONTROL, 'a')
                    msg_box.clear()
                    msg_box.send_keys(message)
                    return True  # Typing succeeded
                except Exception as e:
                    print(f"Attempt {attempt + 1}: Typing failed, retrying...")
                    print(f"Error: {str(e)}")
                    time.sleep(delay)
            return False  # Typing failed after max_attempts
        
        if "switch-on" in pre_order_switch_class and not replace:
            print("Already switched on Preorder Product Setting")
            return
        
        if "switch-off" in pre_order_switch_class or replace:
            if not self.switch_click_handler(driver, pre_order_switch):
                msg = "Switch click failed after multiple attempts."
                print(msg)
                logging.error(msg)
                return
            
            print("Switch clicked successfully.")
            print("Switched on Preorder Product Setting")

        pre_order_msg_chinese, pre_order_msg_english = self.period_type_handler(period_type)
        
        english_msg_box = driver.find_element(By.XPATH, self.xpath_selector("Setting_tab", "english_msg_box"))
        chinese_msg_box = driver.find_element(By.XPATH, self.xpath_selector("Setting_tab", "chinese_msg_box"))
        
        if type_in_msg_box(driver, english_msg_box, pre_order_msg_english):
            msg = "Typed in Preorder Product Note (English)"
            print(msg)
            logging.info(msg)
        else:
            msg = "Typing Preorder Product Note (English) failed after multiple attempts."
            print(msg)
            logging.error(msg)
        if type_in_msg_box(driver, chinese_msg_box, pre_order_msg_chinese):
            msg = "Typed in Preorder Product Note (Chinese)"
            print(msg)
            logging.info(msg)
        else:
            msg = "Typing Preorder Product Note (Chinese) failed after multiple attempts."
            print(msg)
            logging.error(msg)
    
    def save_button_handler(self, driver, max_attempts=8, delay=1) -> None:
        msg = "Saved changes, completed"
        save_button_xpath = self.xpath_selector("actions", "save_button")

        for attempt in range(max_attempts):
            try:
                driver.find_element(By.XPATH, save_button_xpath).click()
                print(msg)
                logging.info(msg)
                return
            except Exception as e:
                error_msg = f"Attempt {attempt + 1}: Save button click failed, retrying..."
                print(error_msg)
                logging.error(error_msg)
                print(f"Error: {str(e)}")
                time.sleep(delay)
        print("Save button click failed after multiple attempts.")

    def pre_order_close_action(self, process_list, driver) -> None:
        mode = "close"
        
        for sku_id, has_variant, chinese_name in process_list:
            print("Now browsing to " + chinese_name +", SKU: " + sku_id)
            driver.get(self.config_url()+"products/"+sku_id+"/edit")
            driver.implicitly_wait(10)

            #Go to tab to turn off accept order option when back in stock
            if has_variant is False:
                #the product doesnt have any variations, go to Price and Qty Tab
                key = "PriceQuantity"
                self.tab_click(driver, key)
                pre_order_button_xpath = self.xpath_selector(key+"_tab", "pre_order_button")
                self.pre_order_click(driver, key, pre_order_button_xpath, mode)
            else:
                #the product has variations, go to Variations Tab
                key = "Variations"
                self.tab_click(driver, key)
                pre_order_button_xpath = self.xpath_selector(key+"_tab", "pre_order_button")
                self.pre_order_click(driver, key, pre_order_button_xpath, mode)

            #Go to Setting tab for type in pre order message
            self.tab_click(driver, "Setting")
            self.pre_order_switch_off_handler(driver)       

            #Save after changes
            self.save_button_handler(driver)

    def pre_order_open_action(self, process_list, driver, replace) -> None:
        mode = "open"

        for sku_id, has_variant, period_type, chinese_name in process_list:
            print("Now browsing to " + chinese_name +", SKU: " + sku_id)
            driver.get(self.config_url()+"products/"+sku_id+"/edit")
            driver.implicitly_wait(10)

            #Go to tab to turn on accept order option when out of stock
            if has_variant is False:
                #the product doesnt have any variations, go to Price and Qty Tab
                key = "PriceQuantity"
                self.tab_click(driver, key)
                pre_order_button_xpath = self.xpath_selector(key+"_tab", "pre_order_button")
                self.pre_order_click(driver, key, pre_order_button_xpath, mode)
            else:
                #the product has variations, go to Variations Tab
                key = "Variations"
                self.tab_click(driver, key)
                pre_order_button_xpath = self.xpath_selector(key+"_tab", "pre_order_button")
                self.pre_order_click(driver, key, pre_order_button_xpath, mode)

            #Go to Setting tab for type in pre order message
            self.tab_click(driver, "Setting")
            self.pre_order_switch_on_handler(driver, period_type, replace)

            #Save after changes
            self.save_button_handler(driver)

    def PreOrderClose(self) -> None:
        driver = self.webdriver.get_driver()
        process_list = []
        self.shopline_login(driver)
        time.sleep(3)
        driver.get(self.api_url() + 'products?page=1&offset=0&limit=1000&scope=preorder')       
        time.sleep(3)
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
            has_variant = False
            if len(item["variations"]) > 0:
                has_variant = True

            if int(quantity) > 0 and status == "active" and is_preorder == True:
                print(chinese_name)
                process_list.append([sku_id, has_variant, chinese_name])
        
        print("Process items: ")
        print(process_list) 
        logging.info("process_list as following")
        logging.info(process_list)
        print("total items to execute: " + str(len(process_list)))
        self.pre_order_close_action(process_list, driver)
        print("All Completed, End Task.")

    def PreOrderOpen(self) -> None:
        driver = self.webdriver.get_driver()
        process_list = []
        self.shopline_login(driver)
        data = self.xls_to_list('search/namelist.xls')
        data.pop(0)
        search_for = dict([[row[0], row[1]] for row in data])
        exclude_list = self.xls_to_list('search/exclude.xls')
        exclude_list.pop(0)
        exclude_list_items = [item for sublist in exclude_list for item in sublist]
        print("Your exclude list:")
        print(exclude_list_items)
        print("You can edit the exclude list under 'search/' folder")
        print("items found: ")
        time.sleep(3)

        for key in search_for.keys():
            time.sleep(0.5)
            driver.get(self.api_url() + 'products?page=1&offset=0&limit=10000&query='+ key +'&scope=search')
            html_response = driver.find_element(By.XPATH, '/html/body/pre').text
            json_data = json.loads(html_response)

            if 'data' in json_data and 'items' in json_data['data']:
                product_items = json_data['data']['items']
            else:
                product_items = []

            for item in product_items:
                quantity = item['quantity']
                status = item['status']
                is_preorder = item['is_preorder']
                sku_id = item['id']
                chinese_name = item['title_translations']['zh-hant']
                has_variant = False
                if len(item["variations"]) > 0:
                    has_variant = True

                not_discounted = False
                if item['tags_array'] is None:
                    not_discounted = True
                elif item['sku'] is None or 'dis' not in item['tags_array'] or 'dis' not in item['sku']:
                    not_discounted = True

                if not_discounted == True:
                    if quantity <= 0 and not is_preorder and status == "active":
                        is_duplicate = any(item[0] == sku_id for item in process_list)
                        if not is_duplicate:
                            not_in_exclude_list = all(chinese_name not in item for item in exclude_list)
                            if not_in_exclude_list:
                                print(chinese_name)
                                process_list.append([sku_id, has_variant, search_for[key], chinese_name])

        print("Collected data....")
        print("Process items: ")
        print(process_list) 
        logging.info("process_list as following")
        logging.info(process_list)
        print("total items to execute: " + str(len(process_list)))
        replace = False
        self.pre_order_open_action(process_list, driver, replace)
        print("All Completed, End Task.")
        self.webdriver.close_driver()

    def PreOrderCloseKeywords(self) -> None:
        print("Please wait for the data loaded...")
        driver = self.webdriver.get_driver()  
        self.shopline_login(driver)
        time.sleep(3)
        driver.get(self.api_url() + 'products?page=1&offset=0&limit=1000&scope=preorder')
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
            has_variant = False
            print()
            if len(item["variations"]) > 0:
                has_variant = True
            
            if keyword in chinese_name:
                process_list.append([sku_id, has_variant, chinese_name])

        print("Process items: ")
        print(process_list) 
        print("total items to execute: " + str(len(process_list)))
        logging.info("process_list as following")
        logging.info(process_list)
        self.pre_order_close_action(process_list, driver)
        print("Task Complete")
        self.webdriver.close_driver()

    def FindMissingPreOrderOpen(self, products_limit=5000) -> None:
        driver = self.webdriver.get_driver()
        self.shopline_login(driver)
        time.sleep(3)
        print("Please wait....")
        api_url = self.api_url() + "products?page=1&offset=0&limit="+ products_limit + "&scope=search"
        driver.get(api_url)
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)
        product_items = json_data['data']['items']
        print("total items found: " + str(len(product_items)))

        open_preorder_process_list = []
        close_preorder_process_list = []

        data = self.xls_to_list('search/namelist.xls')
        data.pop(0)
        #search_for = dict([[row[0], row[1]] for row in data])

        for item in product_items:
            chinese_name = ""
            try:
                chinese_name = item['title_translations']['zh-hant']
            except KeyError as e:
                chinese_name = item['title_translations']['en']
            sku_id = item['_id']
            quantity = item['quantity']
            is_preorder = item['is_preorder']
            out_of_stock_orderable = item['out_of_stock_orderable']
            status = item['status']

            has_variant = len(item.get('variations', [])) > 0

            not_discounted = (
                item['tags_array'] is None
                or item['sku'] is None
                or 'dis' not in item['tags_array']
                or 'dis' not in item['sku']
            )

            close_msg = chinese_name + " is added to close pre oreder"
            open_msg = chinese_name + " is added to open pre oreder"

            if status == "active":
                if is_preorder and out_of_stock_orderable:
                    if quantity > 0:
                        print(close_msg)
                        logging.info(close_msg)
                        close_preorder_process_list.append([sku_id, has_variant, chinese_name])
                    else:
                        if not_discounted is False:
                            print(close_msg)
                            logging.info(close_msg)
                            close_preorder_process_list.append([sku_id, has_variant, chinese_name])
                        else:
                            print(open_msg)
                            logging.info(open_msg)
                            open_preorder_process_list.append([sku_id, has_variant, "C", chinese_name])
                elif not is_preorder and out_of_stock_orderable:
                    if not_discounted is False:
                        print(close_msg)
                        logging.info(close_msg)
                        close_preorder_process_list.append([sku_id, has_variant, chinese_name])
                    else:
                        print(open_msg)
                        logging.info(open_msg)
                        open_preorder_process_list.append([sku_id, has_variant, "C", chinese_name])
                elif not is_preorder and not out_of_stock_orderable:
                    pass  # Irrelevant, skip
                elif is_preorder and not out_of_stock_orderable:
                    close_preorder_process_list.append([sku_id, has_variant, chinese_name])
            else:
                pass

        print("Process Open Pre-order items: ")
        print(open_preorder_process_list)
        print("total items to execute: " + str(len(open_preorder_process_list)))
        logging.info("process_list as following")
        logging.info(open_preorder_process_list)
        replace = False
        self.pre_order_open_action(open_preorder_process_list, driver, replace)

        print("Process Close Pre-order items: ")
        print(close_preorder_process_list)
        print("total items to execute: " + str(len(close_preorder_process_list)))
        logging.info("process_list as following")
        logging.info(close_preorder_process_list)
        self.pre_order_close_action(close_preorder_process_list, driver)

        print("Find Missing Pre-Order Task Complete")
        self.webdriver.close_driver()

    def PreOrderDescriptionForceUpdate(self) -> None:
        print("Please wait for the data loaded...")
        driver = self.webdriver.get_driver()
        self.shopline_login(driver)
        time.sleep(3)
        driver.get(self.api_url() + 'products?page=1&offset=0&limit=1000&scope=preorder')
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)
        product_items = json_data['data']['items']
        print("total items found: " + str(len(product_items)))
        keyword = input("Please input the keywords or exact product Chinese name: ")
        logging.info('Submitted keyword: ' + keyword)
        key_period = input("Please input the period that you would like to update (A-E or NA): ")
        logging.info('Submitted period: ' + key_period)
        process_list = []

        # Loop through each item in the JSON data and check if the keyword matches any value in the "title_translations" dictionary
        for item in product_items:
            chinese_name = item['title_translations']['zh-hant']
            sku_id = item['id']
            has_variant = False
            print()
            if len(item["variations"]) > 0:
                has_variant = True
            
            if keyword in chinese_name:
                is_duplicate = any(item[0] == sku_id for item in process_list)
                if not is_duplicate:
                    process_list.append([sku_id, has_variant, key_period, chinese_name])

        print("Collected data....")
        print("Process items: ")
        print(process_list) 
        logging.info("process_list as following")
        logging.info(process_list)
        print("total items to execute: " + str(len(process_list)))
        replace = True
        self.pre_order_open_action(process_list, driver, replace)
        print("All Completed, End Task.")