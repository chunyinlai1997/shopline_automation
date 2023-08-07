from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from datetime import datetime
import multiprocessing
import json
import time
import csv
import logging
import os

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
        with open(sourcefile, 'r', encoding='utf-8', errors='ignore') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row (if present)
            next(reader)
            # Extract the desired columns and add to the list
            for row in reader:
                first_column = row[0]
                third_column = row[2]
                fourth_column = row[3]
                fifth_column = row[4]
                extracted_values.append([first_column, third_column, fourth_column, fifth_column])

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

    def product_dropdown_handler(self, driver, google_product_category, google_feed_options, google_feed_3rdlayer_options):
        print("Google Category:", google_product_category, google_feed_options, google_feed_3rdlayer_options)
        
        def select_option_by_value(element, value):
            slected = False
            counter = 0
            while not slected or counter>5:
                try:
                    dropdown = Select(element)
                    dropdown.select_by_value(value)
                    slected = True
                    time.sleep(0.5)
                except NoSuchElementException or StaleElementReferenceException:
                    counter += 1
                    logging.debug("unable to select")
        
        dropdown_element_agegroup = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/div/product-form-feed/div[4]/div[2]/div[1]/div[2]/div/select")
        select_option_by_value(dropdown_element_agegroup, "string:adult")
        
        dropdown_element_adult = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[3]/div/product-form-feed/div[4]/div[2]/div[1]/div[3]/div/select")
        select_option_by_value(dropdown_element_adult, "string:yes")
        
        dropdown_element_google_product_category = driver.find_element(By.ID, "google_feed_categories")
        select_option_by_value(dropdown_element_google_product_category, google_product_category)
        
        dropdown_element_google_feed_options = driver.find_element(By.ID, "google_feed_options")
        select_option_by_value(dropdown_element_google_feed_options, google_feed_options)
        
        dropdown_element_google_feed_3rdlayer_options = driver.find_element(By.ID, "google_feed_3rdlayer_options")
        select_option_by_value(dropdown_element_google_feed_3rdlayer_options, google_feed_3rdlayer_options)


    def UpdateGoogleCategory(self, process_list, num_processes):
        # Split process_list into smaller chunks for each process
        chunk_size = len(process_list) // num_processes
        process_chunks = [process_list[i:i + chunk_size] for i in range(0, len(process_list), chunk_size)]

        # Create a list to store the processes
        processes = []

        # Create and start each process
        for chunk in process_chunks:
            process = multiprocessing.Process(target=self.process_chunk, args=(chunk,))
            process.start()
            processes.append(process)

        # Wait for all processes to finish
        for process in processes:
            process.join()
        
        print("All subprocesses completed, end of work.")
        
    def process_chunk(self, sub_process_list):
        print("Processing chuck items:", len(sub_process_list))
        driver = webdriver.Chrome()

        self.shopline_login(driver)

        for sku_id, cat1, cat2, cat3 in sub_process_list:
            time.sleep(1)
            print("Now Processing:", sku_id)
            driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
            try:
                button_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[1]/div/span[2]/button'
                product_save_button = driver.find_element(By.XPATH, button_xpath) 
                driver.get("https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products/"+sku_id)
                scrawled_category = False
                while not scrawled_category:
                    html_response = driver.find_element(By.XPATH, '/html/body/pre').text
                    json_data = json.loads(html_response)
                    try:
                        google_3rd_layer_option_id = json_data['data']['feed_category']['google_3rd_layer_option_id']
                        if google_3rd_layer_option_id is None:
                            logging.debug(sku_id + "unable to crawl the google_3rd_layer_option_id")
                        else:
                            scrawled_category = True   
                    except TypeError or AttributeError:
                        google_3rd_layer_option_id = "empty"
                        scrawled_category = True
                         
                print(sku_id + "is in " + google_3rd_layer_option_id)

                if "string:"+google_3rd_layer_option_id == cat3:
                    print(sku_id + " already in correct category")
                else: 
                    driver.implicitly_wait(1)
                    driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")
                    print("Go to Product Feed Data Tab")
                    self.product_feed_data_button_handler(driver)
                    print("Change Dropdown Element Values")
                    self.product_dropdown_handler(driver, cat1, cat2, cat3)
                    #Save after changes
                    try:    
                        product_save_button = driver.find_element(By.XPATH, button_xpath) 
                        product_save_button.click()
                        print(sku_id + "Saved changes, completed")
                    except NoSuchElementException or StaleElementReferenceException:
                        message = sku_id = " completed but unable to save!"
                        print(message)
                        logging.error(message)

            except NoSuchElementException or StaleElementReferenceException:
                print("Switch to Product Set")
                driver.get("https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products/"+sku_id+"?filters%5B%5D=related_products_all&force_with_product_set=true&includes%5B%5D=retail_price&with_flash_price_campaign=true")
                scrawled_category = False
                while not scrawled_category:
                    html_response = driver.find_element(By.XPATH, '/html/body/pre').text
                    json_data = json.loads(html_response)
                    try:
                        google_3rd_layer_option_id = json_data['data']['feed_category']['google_3rd_layer_option_id']
                        if google_3rd_layer_option_id is None:
                            logging.warning(sku_id + "unable to crawl the google_3rd_layer_option_id")
                        else:
                            scrawled_category = True   
                    except TypeError or AttributeError:
                        google_3rd_layer_option_id = "empty"
                        scrawled_category = True
                
                print(sku_id + "is in " + google_3rd_layer_option_id)

                if "string:"+google_3rd_layer_option_id == cat3:
                    print(sku_id + " already in correct category")
                else:
                    driver.get("https://admin.shoplineapp.com/admin/waddystore/product_sets/"+sku_id+"/edit")
                    driver.implicitly_wait(3)
                    print("Go to Product Set Feed Data Tab")
                    self.product_set_feed_data_button_handler(driver)
                    print("Change Dropdown Element Values")
                    self.product_dropdown_handler(driver, cat1, cat2, cat3)
                    #Save after changes
                    button_xpath = '/html/body/div[3]/div[2]/div[1]/div[1]/div/div[2]/form/div[1]/div[1]/div/span[2]/button'
                    try:    
                        product_save_button = driver.find_element(By.XPATH, button_xpath) 
                        product_save_button.click()
                        print(sku_id + "Saved changes, completed")
                    except NoSuchElementException or StaleElementReferenceException:
                        message = sku_id = " completed but unable to save!"
                        print(message)
                        logging.error(message)  
        print("Process Chuck Completed") 

if __name__ == "__main__":
    # Create the log folder if it doesn't exist
    if not os.path.exists('log'):
        os.makedirs('log')
    now = datetime.now()
    log_file = f'log/google_category_update_{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    multiprocessing.freeze_support()
    google_category_clicks = Google_Category_Clicker()
    item_list = google_category_clicks.csv_to_list('issue_google_products.csv')
    num_processes = eval(input("How many number of processes required? (Input in number): "))
    google_category_clicks.UpdateGoogleCategory(item_list, num_processes)