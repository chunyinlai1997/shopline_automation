from flask import Flask, render_template, request
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route('/click') 
def click():
    #username = request.form.get("user_name")
    #password = request.form.get("password") 
    
    username = "info@waddystore.com"
    password = "Waddy1208"

    driver = webdriver.Chrome(keep_alive=True)
    driver.set_window_size(1100, 800)

    #login admin account

    driver.get('https://admin.shoplineapp.com/admin/waddystore/')
    driver.find_element(By.ID, "staff_email").send_keys(username)
    driver.find_element(By.ID, "staff_password").send_keys(password)
    driver.find_element(By.ID, "reg-submit-button").click()

    #go to pre-order page
    driver.get("https://admin.shoplineapp.com/admin/waddystore/products?page=1&with_flash_price_campaign=true&scope=preorder")

    
    #table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div/div[4]/div/div[2]/div[4]/table/tbody")
    #rows = table.find_elements(By.TAG_NAME, "tr")
    #for row in rows:
    #    print(row)
    #table = table_div.find_element(By.TAG_NAME, "table")
    #print(table)
    #rows = table.find_elements(By.TAG_NAME, "tr")
    
    driver.implicitly_wait(20)





