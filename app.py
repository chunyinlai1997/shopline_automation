from flask import Flask, render_template, request
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
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

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1100, 800)

    driver.get('https://admin.shoplineapp.com/admin/waddystore/')

    driver.find_element("id", "staff_email").send_keys(username)
    driver.find_element("id", "staff_password").send_keys(password)
    driver.find_element("id",'reg-submit-button').click()
    
    driver.implicitly_wait(20)

    driver.get('https://admin.shoplineapp.com/admin/waddystore/products')

    wait = WebDriverWait(driver, 10)
    






