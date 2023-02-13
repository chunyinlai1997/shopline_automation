from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class Action():
    def __init__(self):
        pass

    def pre_order_button_handler(self, driver, button_path, mode):
        accept_button = driver.find_element(By.XPATH, button_path)
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
                    print("ElementNotInteractableException")
                    return False
                except NoSuchElementException:
                    print("NoSuchElementException")
                    return False
            else:
                pass
        elif mode == "close":
            if accept_button_status == True or accept_button_status == "true":
                print("clicking checkbox")
                try:
                    driver.find_element(By.XPATH,button_path).click()
                except ElementNotInteractableException:
                    print("ElementNotInteractableException")
                    return False
                except NoSuchElementException:
                    print("NoSuchElementException")
                    return False              
            elif accept_button_status == None:
                print("pass clicking checkbox, already unchecked")
            else:
                pass
        
        return True
            
    def open_preorder(self, process_list: list):
        driver = webdriver.Chrome(keep_alive=True)
        driver.set_window_size(1100, 800)
        print("Clicker starts")
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        driver.find_element(By.ID, "reg-submit-button").click()
        print("Login sucessful")
        
        for sku_id, bar, has_varient, period_type in process_list:
            print("Now browsing to SKU: " + sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            print(bar, period_type)
            driver.implicitly_wait(10)
            if has_varient is False:
                driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
                print("Go to Price and Quantity Tab")
                xpath = '//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input'
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

            
            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
            print("Go to Settings Tab")

            pre_order_switch = driver.find_element(By.XPATH, '//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
            pre_order_switch_classess = pre_order_switch.get_attribute("class")
            if "switch-off" in pre_order_switch_classess:
                print("Not yet switched on Preorder Product Setting")
                ActionChains(driver).move_to_element(pre_order_switch).click().perform()
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
            elif "switch-on" in pre_order_switch_classess:
                print("Already switched on Preorder Product Setting")
            else:
                print("ERROR, switch not found")

            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
            print("Saved changes, completed")

    def close_preorder(self, process_list):
        driver = webdriver.Chrome(keep_alive=True)
        driver.set_window_size(1100, 800)
        print("Clicker starts")
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)
        driver.find_element(By.ID, "reg-submit-button").click()
        print("Login sucessful")

        for sku_id, bar, has_varient in process_list:
            print("Now browsing to SKU: " + sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            driver.implicitly_wait(15)

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

        
            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
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
        
