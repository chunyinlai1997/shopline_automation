import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Transfer():
    def __init__(self) -> None:
        pass

    def shopline_login(self, driver):
        username = "info@waddystore.com"
        password = "Waddy1208"
        driver.get('https://admin.shoplineapp.com/admin/waddystore/')
        time.sleep(2)
        staff_email_id = "staff_email"
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.ID, staff_email_id)))
        driver.find_element(By.ID, staff_email_id).send_keys(username)
        time.sleep(2)
        driver.find_element(By.ID, "staff_password").send_keys(password)

        while True:
            try:
                time.sleep(2)
                submit_btn = driver.find_element(By.XPATH, '//*[@id="reg-submit-button"]')
                submit_btn.click()
            except:
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
                human = input("Please type 'ok' when done: ")
            
            # Wait for the new page to load
            wait.until(EC.staleness_of(driver.find_element_by_tag_name('html')))
    
    def dbee_login(self, driver):
        dbee_username = "waddystore@gmail.com"
        dbee_password = "Waddy304"
        driver.get('https://wms.dbee.hk/login')
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(dbee_username)
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(dbee_password)
        driver.find_element(By.XPATH, '//*[@id="submit"]').click()
        print("Login Dbee sucessful")
    
    def get_inventory_tranfer_json(self, driver):
        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/pos/inventory_transfers?page=1&offset=0&limit=100')
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)
        return json_data
    
    def change_inventory_transfer_status(self, driver, transfer_id):
        driver.get('https://admin.shoplineapp.com/admin/waddystore/inventory_transfer/'+ transfer_id)
        change_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/react-app/div/div[1]/div[2]/div[2]/button')
        change_button.click()
        time.sleep(5)
        change_button_2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/react-app/div/div[1]/div[2]/div[2]/div/div[2]/div[3]/button[2]')
        ask = input("real or fake submit? REAL = submit : ")
        if ask.lower() == 'real':
            change_button_2.click()
        else:
            print("fake submitted in dbee")
        print("shopline inventory transfer status changed.")
    
    def transfer_ops(self):
        driver = webdriver.Chrome()
        
        self.shopline_login(driver)
        self.dbee_login(driver)

        json_data = self.get_inventory_tranfer_json(driver)
        transfers= json_data['items']

        attribute_name = "status"
        attribute_value = "pending"
        filtered_transfer = [x for x in transfers if x[attribute_name] == attribute_value]
        for transfer in filtered_transfer:
            destination = transfer['destination']['name']['zh-hant']
            origin = transfer['origin']['name']['zh-hant']
            transfer_number = transfer['number']
            transfer_id = transfer['id']
            items = transfer['items']
            recipient_contacts = {
                "深水埗店": "55415830",
                "尖沙咀店": "52957961"
            }

            if origin == "HKTV (網店)":
                print("Transfer from HKTV stock, skip process")
            elif origin == "網店倉庫":
                if destination == "HKTV (網店)":
                    print("Transfer from warehouse to HKTV stock, no warehouse order")
                elif destination == "網店倉庫":
                    print("Transfer from warehouse to warehouse, Error!")      
                elif destination == "深水埗店" or destination == "尖沙咀店":
                    #open dbee order
                    print("Transfer from warehouse to shop " + destination)
                    print("調撥單: "+ transfer_number)

                    driver.get("https://wms.dbee.hk/order/create")
                    deliver_carrier = driver.find_element(By.ID, "deliver_carrier")
                    select = Select(deliver_carrier)
                    select.select_by_index(4)
                    assert select.first_selected_option.text == "自取-荃灣倉 (客人及司機)"
                    recipient_name = driver.find_element(By.ID, "recipient_name")
                    shop_name = "Waddy Store " + str(destination) 
                    recipient_name.send_keys(shop_name)
                    recipient_contact = driver.find_element(By.ID, "recipient_contact")
                    
                    # set the recipient contact based on the destination
                    if destination in recipient_contacts:
                        recipient_contact.send_keys(recipient_contacts[destination])
                    else:
                        # handle the case where the destination is not in the dictionary
                        print(f"Error: Unknown destination '{destination}'.")
                    
                    recipient_comment = driver.find_element(By.ID, "recipient_comment")
                    recipient_comment.send_keys("調撥單往 "+shop_name)
                    order_comment = driver.find_element(By.ID, "order_comment")
                    order_comment.send_keys("調撥單 no. "+transfer_number)
                    is_complete = False

                    for num in range(0, len(items)):
                        sku_barcode_id = "items-" + str(num) + "-barcode"
                        sku_amount_id = "items-" + str(num) + "-amount"
                        sku_barcode = driver.find_element(By.ID, sku_barcode_id)
                        sku_barcode.send_keys(items[num]["gtin"])
                        driver.implicitly_wait(20)
                        sku_barcode.send_keys(Keys.ARROW_UP)  
                        sku_barcode.send_keys(Keys.ARROW_UP)
                        sku_barcode.send_keys(Keys.ENTER)   
                        sku_amount = driver.find_element(By.ID, sku_amount_id) 
                        sku_amount.send_keys(items[num]["quantity"])
                        if num + 1 == len(items):
                            driver.find_element(By.XPATH,'//*[@id="calc_price"]').click()
                            is_complete = True
                        else:
                            driver.find_element(By.XPATH,'//*[@id="add-item"]').click()
                    
                    while True:
                        try:
                            final_button = driver.find_element(By.XPATH, '//*[@id="calc_price"]')
                            if final_button:
                                final_button.click()
                                print("Transfer order ", transfer_number, " completed.")
                                break
                        except Exception as e:
                            print("An error occurred:", e)
                            response = input("Do you want to continue? (Y/N) ")
                            if response.lower() == "y":
                                final_button.click()
                                print("Transfer order ", transfer_number, " completed.")
                                break
                            else:
                                break  # exit the loop if user chooses not to continue

            elif origin == "深水埗店" or origin == "尖沙咀店":
                if destination == "HKTV (網店)":
                    print("Transfer from shop", origin, "to HKTV stock, only manual warehouse stock in")
                elif destination == "深水埗店" or destination == "尖沙咀店":
                    print("Transfer from shop", origin,"to", destination, " , no warehouse stock in")
                elif destination == "網店倉庫":
                    print("Transfer from shop", origin, "to warehouse")
                    #open dbee stock in
                    driver.get("https://wms.dbee.hk/stock/in/create")
                    comment = driver.find_element(By.XPATH, '//*[@id="comment"]')
                    comment.send_keys("調撥單 no. "+transfer_number)
                    ref_comment = driver.find_element(By.XPATH, '//*[@id="stock_in_delivery_reference"]')
                    ref_comment.send_keys(origin + " 調貨到倉庫,調撥單 no. " + transfer_number)
                    date_input = driver.find_element(By.XPATH,'//*[@id="stock_in_arrival_date"]')
                    date_input.clear()
                    today = datetime.today()
                    next_week = today + timedelta(days=7)   
                    date_string = next_week.strftime("%d-%m-%Y")
                    date_input.send_keys(date_string)
                    print("調撥單: ", transfer_number)

                    for i, item in enumerate(items):
                        sku_barcode_id = "items-" + str(i) + "-barcode"
                        sku_amount_id = "items-" + str(i) + "-amount"
                        sku_barcode = driver.find_element(By.ID, sku_barcode_id)
                        sku_barcode.send_keys(items[i]["gtin"])
                        driver.implicitly_wait(20)
                        sku_barcode.send_keys(Keys.ARROW_UP)  
                        sku_barcode.send_keys(Keys.ARROW_UP)
                        sku_barcode.send_keys(Keys.ENTER)   
                        sku_amount = driver.find_element(By.ID, sku_amount_id) 
                        sku_amount.send_keys(0) 
                        sku_amount.send_keys(items[i]["quantity"])

                        if i == len(items) - 1:
                            break
                        else:
                            add_item_button = driver.find_element(By.XPATH, '//*[@id="add-item"]')
                            add_item_button.click()
                    
                    ask = input("real submit or fake? REAL = submit : ")
                    if ask.lower() == 'real':
                        driver.find_element(By.XPATH,'//*[@id="submit"]').click()
                    else:
                        print("fake submitted in dbee")
                    
                    self.change_inventory_transfer_status(driver, transfer_id)
