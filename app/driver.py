import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class WebDriver:
    def __init__(self):
        self.current_os = platform.system()
        self.driver = None

    def create_driver(self):
        self.driver = webdriver.Chrome(service=ChromeService( ChromeDriverManager().install()))

    def get_driver(self):
        if not self.driver:
            self.create_driver()
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None