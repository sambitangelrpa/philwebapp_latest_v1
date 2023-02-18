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

class Ecb_PDF_Scraping:

    def __init__(self):
        self.ecb_link = "https://www.ecb.europa.eu/press/key/date/html/index.en.html"
        selenium_obj = Selenium_Run(self.ecb_link)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        self.filename="./Scraped_Data/ECB_PDF_Link.xlsx"

    def pdf_link_scrape(self):
        existed_pdf_data = pd.read_excel(self.filename)

        existed_pdf_data['date'] = pd.to_datetime(existed_pdf_data['date'], format='%d %B %Y')

        df = pd.DataFrame(columns=["date", "link", "title"])

        # action = ActionChains(self.driver)
        for i in range(2):

            time.sleep(5)
            date = [i.text for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dt/div')))]
            #     print(date)
            link = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dd/div/a')))]
            #     print(link)
            title = [i.text for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dd/div[1]/a')))]

            for date, link, title in zip(date, link, title):
                #         print(link)

                df.loc[len(df.index)] = [date, link, title]

        df['date'] = pd.to_datetime(df['date'], format='%d %B %Y')
        # df.head(10)
        df = df[df['link'].str.contains("pdf")]
        # df
        latest_date = existed_pdf_data['date'][0]
        df = df[df['date'] > latest_date]
        existed_pdf_data = pd.concat([df, existed_pdf_data], ignore_index=True)

        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Write the DataFrame to the Excel file
        existed_pdf_data.to_excel('./Scraped_Data/ECB_PDF_Link.xlsx',encoding='ascii',index=False)


if __name__=='__main__':

    obj=Ecb_PDF_Scraping()
    obj.pdf_link_scrape()