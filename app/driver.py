import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class WebDriver:
    def __init__(self):
        self.current_os = platform.system()
        self.driver = None

    def create_driver(self):
        ch_options = Options()
        #ch_options.add_argument("--headless")
        ch_options.add_experimental_option("prefs", {
        "download.default_directory": r"tmp",
        "download.prompt_for_download": False
        })

        chrome_service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=ch_options)

    def get_driver(self):
        if not self.driver:
            self.create_driver()
        return self.driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None