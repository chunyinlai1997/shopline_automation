from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import logging

class ShoplineLoginHandler():

    def __init__(self, config_path='config.json'):
        self.config_path = config_path

    def read_config(self):
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    
    def shopline_login(self, driver):
        config = self.read_config()
        username = config["username"]
        password = config["password"]
        login_url = config["login_url"]

        driver.get(login_url)
        driver.find_element(By.ID, "staff_email").send_keys(username)
        driver.find_element(By.ID, "staff_password").send_keys(password)

        wait = WebDriverWait(driver, 120)

        while True:
            try:
                time.sleep(2)
                submit_btn = driver.find_element(By.XPATH, '//*[@id="reg-submit-button"]')
                submit_btn.click()
            except:
                logging.debug("Unable to log in automatically, blocked by Captcha")
                print("Unable to log in automatically.")

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
                logging.debug("There is still blocking or captcha issue")
                human = input("Please type 'ok' when done: ")

            # Wait for the new page to load
            wait.until(EC.staleness_of(driver.find_element_by_tag_name('html')))
