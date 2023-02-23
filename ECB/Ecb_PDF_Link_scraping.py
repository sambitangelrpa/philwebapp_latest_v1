from common.run_selenium import Selenium_Run
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from common.run_selenium import Selenium_Run
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
    """
                     This is a Python class called Ecb_PDF_Scraping which is used to scrape the ECB (European Central Bank) website for
                     PDF files containing speeches or other key information. The class uses the Selenium web driver to automate browsing
                    the ECB website and extract links to PDF files. The extracted links are then saved in an Excel file located in the Scraped_Data folder.

                     Written By: OBI
                     Version: 1.0
                     Revisions: None

    """

    def __init__(self):
        self.ecb_link = "https://www.ecb.europa.eu/press/key/date/html/index.en.html"
        selenium_obj = Selenium_Run(self.ecb_link)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        self.filename="../Scraped_Data/ECB_PDF_Link.xlsx"

    def pdf_link_scrape(self):

        """
                    Method Name: pdf_link_scrape
                    Description: This method is part of the Ecb_PDF_Scraping class and is responsible for scraping the links
                                to ECB PDF files from the ECB website, and updating an Excel file with the new links.
                    Output: Scraped_Data/ECB_PDF_Link.xlsx
                    On Failure: Exception

                    Written By: OBI
                    Version: 1.0
                    Revisions: None

        """
        try:

            existed_pdf_data = pd.read_excel(self.filename)

            existed_pdf_data['date'] = pd.to_datetime(existed_pdf_data['date'], format='%d %B %Y')

            df = pd.DataFrame(columns=["date", "link", "title"])

            # action = ActionChains(self.driver)
            for i in range(1):

                time.sleep(5)
                date = [i.text for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dt/div')))]

                link = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dd/div/a')))]

                title = [i.text for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="snippet{i}"]/dd/div[1]/a')))]

                for date, link, title in zip(date, link, title):


                    df.loc[len(df.index)] = [date, link, title]

            df['date'] = pd.to_datetime(df['date'], format='%d %B %Y')

            df = df[df['link'].str.contains("pdf")]
            # df
            latest_date = existed_pdf_data['date'][0]
            df = df[df['date'] > latest_date]

            existed_pdf_data = pd.concat([df, existed_pdf_data], ignore_index=True)

            # Write the DataFrame to the Excel file
            existed_pdf_data.to_excel(self.filename,encoding='ascii',index=False)
        except Exception as e:
            print(e)


if __name__=='__main__':

    obj=Ecb_PDF_Scraping()
    obj.pdf_link_scrape()