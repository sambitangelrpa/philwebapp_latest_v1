from run_selenium import Selenium_Run
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from run_selenium import Selenium_Run
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import pypdfium2 as pdfium
import numpy as np

class Ecb_Scraping:
    def __init__(self):
        self.ecb_download_link = "https://www.ecb.europa.eu/press/key/html/downloads.en.html"
        selenium_obj = Selenium_Run(self.ecb_download_link)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        # self.filename="./Scraped_Data/"

    def download_csv(self):
        link = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-wrapper"]/main/div[2]/p[3]/a')))]
        print(link)
        import requests
        with open("./Scraped_Data/ECB_SpeechData.csv", 'wb') as f, \
                requests.get(link[0], stream=True) as r:
            for line in r.iter_lines():
                f.write(line + '\n'.encode())



if __name__=='__main__':

    obj=Ecb_Scraping()
    obj.download_csv()