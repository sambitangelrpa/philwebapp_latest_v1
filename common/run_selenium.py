from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium import webdriver
from selenium.webdriver.chrome import options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class Selenium_Run:
    """
                 This class will be starting the selenium chrome driver for scraping
                 Written By: OBI
                 Version: 1.0
                 Revisions: None

                                         """

    def __init__(self,link):

        self.web_link = link
        # self.chrome_options=options()

    def run_Fed_driver_chrome(self):
        start_time = time.time()

        driver = webdriver.Chrome(ChromeDriverManager().install())
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"

        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-web-security")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.web_link)
        # cookies=driver.find_element(by=By.XPATH,value="/html/body/div[1]/div[1]/div/div/table/tbody/tr[2]/td[3]/button")
        # cookies.click()
        # WebDriverWait(driver,7).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div/div/table/tbody/tr[2]/td[3]/button'))).click()

        time.sleep(6)
        self.driver.refresh()
        return self.driver






