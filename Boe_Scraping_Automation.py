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


class Boe_Scraping:
    def __init__(self):
        self.boe_weblink = "https://www.bankofengland.co.uk/news/speeches"
        selenium_obj = Selenium_Run(self.boe_weblink)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        self.filename="./Scraped_Data/BOE_SpeechData.xlsx"

    def run_boe_scraping(self):
        existing_boe_data = pd.read_excel(self.filename)
        last_date = existing_boe_data['date'][0].date()

        df = pd.DataFrame(columns=["LINKS", "INFO"])

        action = ActionChains(self.driver)

        for _ in range(1):
            time.sleep(5)
            main_speech_links = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="SearchResults"]/div/a')))]
            main_speech_text = [i.text for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="SearchResults"]/div/a')))]
            next_page_eles = [i for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="list-pagination"]/li/a')))]
            time.sleep(5)

            last_page = next_page_eles[-1]
            for link, speech in zip(main_speech_links, main_speech_text):
                df.loc[len(df.index)] = [link, speech]
            action.move_to_element(last_page).click().perform()

        info_list = list(df['INFO'].values)
        ls = []
        for i in info_list:
            ls.append(i.split('\n'))
        df2 = pd.DataFrame(ls, columns=['speaker', 'date', 'title'])
        main_df = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)
        main_df['speaker'] = main_df['speaker'].str.replace(r'Speech //', '')
        main_df.drop(columns=['INFO'], inplace=True)

        main_df['date'] = pd.to_datetime(main_df['date'], format='%d %B %Y')

        final_df = pd.DataFrame()

        for date, link, title, speaker_name in zip(main_df['date'], main_df['LINKS'], main_df['title'],
                                                   main_df['speaker']):

            if (date > last_date):

                self.driver.get(link)
                time.sleep(3)
                try:
                    summary = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '(//span[@class="hero"])[2]'))).text
                except:
                    summary = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, '(//span[@class="hero"])[1]'))).text
                try:
                    try:
                        pdf_link = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, '(//div[@class="content-block"]/div/*/a)[1]'))).get_attribute("href")
                    except:
                        pdf_link = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                            (By.XPATH, '//div[@class="content-block"]/div/a'))).get_attribute("href")
                except:
                    pdf_link = "na"
                try:
                    try:
                        whl_txt = [i.text for i in WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="output"]/section/p')))]
                        whl_txt = " ".join(whl_txt)
                    except:
                        whl_txt = [i.text for i in WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located(
                            (By.XPATH, '//*[@id="main-content"]/section[2]/div/div[1]/div[2]/div/p[2]')))]
                        whl_txt = " ".join(whl_txt)
                except:
                    whl_txt = "na"
                final_df.loc[len(final_df.index), ['date', 'link', 'title', 'speaker_name', 'summary', 'pdf_link',
                                                   'WHOLE_TEXT']] = [date, link, title, speaker_name, summary, pdf_link,
                                                                     whl_txt]

            else:
                break


        rem_links = []
        rem_pdf_links = []
        pdf_df = pd.DataFrame(
            columns=["date", "LINK", "title", "speaker", "summary", "PDF_LINK", "WHL_TEXT", "ALL_TEXT"])

        for date, link, title, speaker, summary, pdf_link, whl_text in zip(final_df['date'], final_df['link'],
                                                                           final_df['title'], final_df['speaker_name'],
                                                                           final_df['summary'], final_df['pdf_link'],
                                                                           final_df['WHOLE_TEXT']):
            print(date)

            if pdf_link != 'na' and len(whl_text) < 350:

                r = requests.get(pdf_link, stream=True)
                os.makedirs("pdfs_new/", exist_ok=True)
                try:
                    try:
                        unq_id = pdf_link.split("=")[-1].strip()
                    except:
                        if pdf_link.endswith(".pdf"):
                            unq_id = pdf_link.split("/")[-1].strip().split(".pdf")[0].strip()
                    chunk_size = 524
                    with open('pdfs_new/' + unq_id + ".pdf", 'wb') as fd:
                        for chunk in r.iter_content(chunk_size):
                            fd.write(chunk)
                    data = r'pdfs_new/' + unq_id + ".pdf"
                    text = ""
                    pdf = pdfium.PdfDocument(data)
                    for i in range(len(pdf)):
                        page = pdf.get_page(i)
                        textpage = page.get_textpage()
                        text += textpage.get_text()
                        [g.close() for g in (textpage, page)]
                    pdf.close()
                    pdf_df.loc[len(pdf_df.index)] = [date, link, title, speaker, summary, pdf_link, whl_text, text]
                except:

                    rem_links.append(link)
                    rem_pdf_links.append(pdf_link)
            else:

                text = np.NAN
                pdf_df.loc[len(pdf_df.index)] = [date, link, title, speaker, summary, pdf_link, whl_text, text]

        pdf_df['WHL_TEXT'] = np.where(pdf_df['WHL_TEXT'] == 'na', pdf_df['ALL_TEXT'], pdf_df['WHL_TEXT'])
        pdf_df.loc[pdf_df['WHL_TEXT'].str.len() < 300, 'WHL_TEXT'] = pdf_df['ALL_TEXT']
        pdf_df.drop(columns=['ALL_TEXT'], inplace=True)

        pdf_df['WHL_TEXT'] = pdf_df['WHL_TEXT'].replace('\n', ' ', regex=True)
        pdf_df['date'] = pd.to_datetime(pdf_df['date']).dt.date

        BOE_data = pd.concat([pdf_df, existing_boe_data], axis=0, ignore_index=True)
        # BOE_data.to_excel('test_Final_All_link_speech_scraping_boe_.xlsx',encoding='ascii',index=False)

        print(BOE_data.head())
        print(BOE_data['WHL_TEXT'].count())


        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Write the DataFrame to the Excel file
        BOE_data.to_excel(self.filename,engine='xlsxwriter',index=False)
        # encoding='utf-8'
if __name__=='__main__':
    obj=Boe_Scraping()
    obj.run_boe_scraping()
