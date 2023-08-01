from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import json
import time
import csv
import logging

class Google_Category_Clicker():

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
    
    def csv_to_list(self, sourcefile):
        # Initialize an empty list to store the extracted values
        extracted_values = []

        # Read the CSV file
        with open(sourcefile, 'r',  encoding='utf-8', errors='ignore') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row (if present)
            next(reader)
            # Extract the first column items and add to the list
            for row in reader:
                first_column = row[0]
                extracted_value = first_column.split(':')[0]
                extracted_values.append(extracted_value)

        # Print the extracted values list
        print("Items found:", len(extracted_values))
        return extracted_values

    def product_feed_data_button_handler(self, driver):
        xpath1 = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/ul/li[9]/a'
        xpath2 = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/ul/li[8]/a'
        tab_found = False
        while tab_found is False:
                try:
                    driver.find_element(By.XPATH, xpath1).click()
                    tab_found = True
                except NoSuchElementException:
                    print("NoSuchElementException for xpath1. Trying xpath2.")
                    try:
                        driver.find_element(By.XPATH, xpath2).click()
                        tab_found = True
                    except NoSuchElementException:
                        print("NoSuchElementException for xpath2. Both xpaths failed.")
                        tab_found = False

    def product_set_feed_data_button_handler(self, driver):
        xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/ul/li[7]/a'
        tab_found = False
        while tab_found is False:
            try:
                driver.find_element(By.XPATH, xpath).click()
                tab_found = True
            except NoSuchElementException:
                print("NoSuchElementException")
                tab_found = False

    def product_dropdown_handler(self, driver):
        #agegroup
        dropdown_element_agegroup = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/div/product-form-feed/div[4]/div[2]/div[1]/div[2]/div/select")
        dropdown_agegroup = Select(dropdown_element_agegroup)
        dropdown_agegroup.select_by_value("string:adult")

        #adult
        dropdown_element_adult = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/div/product-form-feed/div[4]/div[2]/div[1]/div[3]/div/select")
        dropdown_adult = Select(dropdown_element_adult)
        dropdown_adult.select_by_value("string:yes")

        #google_product_category
        dropdown_element_google_product_category = driver.find_element(By.ID, "google_feed_categories")
        dropdown_google_product_category = Select(dropdown_element_google_product_category)
        dropdown_google_product_category.select_by_value("string:mature")

        #google_feed_options
        dropdown_element_google_feed_options = driver.find_element(By.ID, "google_feed_options")
        dropdown_google_feed_options = Select(dropdown_element_google_feed_options)
        dropdown_google_feed_options.select_by_value("string:erotic")

        #google_feed_3rdlayer_options
        dropdown_element_google_feed_3rdlayer_options = driver.find_element(By.ID, "google_feed_3rdlayer_options")
        dropdown_google_feed_3rdlayer_options = Select(dropdown_element_google_feed_3rdlayer_options)
        dropdown_google_feed_3rdlayer_options.select_by_value("string:sex_toys")
        time.sleep(1)

    def product_data(self, sku_id, driver):
        driver.get('https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products/'+ sku_id)
        html_response = driver.find_element(By.XPATH, '/html/body/pre').text
        json_data = json.loads(html_response)

        return True

    def UpdateGoogleCategorySexToy(self, process_list):
        driver = webdriver.Chrome()

        self.shopline_login(driver)
        
        for sku_id in process_list:
            time.sleep(2)
            print("Now Processing:", sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            driver.implicitly_wait(5)
            try: 
                button_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[1]/div/span[2]/button'
                product_save_button = driver.find_element(By.XPATH, button_xpath) 
                print("Go to Product Feed Data Tab")
                self.product_feed_data_button_handler(driver)
                print("Change Dropdown Element Values")
                self.product_dropdown_handler(driver)
                #Save after changes
                product_save_button.click()
                print("Saved changes, completed")
            except NoSuchElementException or StaleElementReferenceException:
                print("Switch to Product Set")
                driver.get("https://admin.shoplineapp.com/admin/waddystore/product_sets/"+sku_id+"/edit")
                driver.implicitly_wait(5)
                print("Go to Product Set Feed Data Tab")
                self.product_set_feed_data_button_handler(driver)
                print("Change Dropdown Element Values")
                self.product_dropdown_handler(driver)
                #Save after changes
                button_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[1]/div/span[2]/button'
                driver.find_element(By.XPATH, button_xpath).click()
                print("Saved changes, completed")     

google_category_clicks = Google_Category_Clicker()
item_list = google_category_clicks.csv_to_list('item_issues.csv')
google_category_clicks.UpdateGoogleCategorySexToy(item_list)