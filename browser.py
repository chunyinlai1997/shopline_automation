from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import pandas as pd
import math
import time

class Action():
    def __init__(self):
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

    def open_preorder(self, sku_id, has_varient):
        print("Now browsing to SKU: " + sku_id)
        driver.get("https://admin.shoplineapp.com/admin/waddystore/products/"+sku_id+"/edit")

        if not has_varient:
            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[4]/a').click()
            print("Go to Price and Quantity Tab")
            accept_button = driver.find_element(By.XPATH,'//*[@id="productForm-pricing"]/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/label/input').get_attribute('checked')
            if accept_button is True:
                print("pass clicking checkbox")
            elif accept_button is None:
                print("clicking checkbox")
                accept_button.click()
        else:
            driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[5]/a').click()
            print("Go to Variations Tab")
            accept_button = driver.find_element(By.XPATH,'//*[@id="productForm-variations"]/div/div[3]/div[3]/div[1]/div/div/div[2]/div/div[5]/label/input').get_attribute('checked')
            if accept_button is True:
                print("pass clicking checkbox")
            elif accept_button is None:
                print("clicking checkbox")
                accept_button.click()

        driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[3]/ul/li[8]/a').click()
        print("Go to Settings Tab")

        pre_order_switch = driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div')
        pre_order_switch_classess = pre_order_switch.get_attribute("class")
        if "switch-on" in pre_order_switch_classess:
            driver.find_element(By.XPATH,'//*[@id="productForm-settings"]/div[1]/div[3]/div[1]/div/div[2]/div/div[1]/div/span[2]').click()
            print("Switched off Preorder Product Setting")
        else:
            print("pass pre-order notice")

        driver.find_element(By.XPATH,'//*[@id="product_form"]/div[1]/div[1]/div/span[2]/button/span[2]').click()
        print("Saved changes, completed")

    def close_preorder(self, sku_id):
        pass
    




