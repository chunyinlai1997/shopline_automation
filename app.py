from flask import Flask, render_template, request
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route('/click') 
def click():
    #username = request.form.get("user_name")
    #password = request.form.get("password") 
    
    username = "willon@waddystore.com"
    password = "Willon97*"

    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver.set_window_size(1100, 800)

    driver.get('https://admin.shoplineapp.com/admin/waddystore/')

    driver.find_element_by_id('staff_email').send_keys(username)
    driver.find_element_by_id('staff_password').send_keys(password)
    driver.find_element_by_id('reg-submit-button').click()
    time.sleep(7)



