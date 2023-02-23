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
import os


class Fed_Scraping:
    """
             This class is used to scrape new speeches from the website of the Federal Reserve Bank of the United States,
              and update the previously scraped data in the file fed_SpeechData.xlsx.

             Written By: OBI
             Version: 1.0
             Revisions: None

                     """

    def __init__(self):
        self.fed_weblink="https://www.federalreserve.gov/newsevents/speeches.htm"
        selenium_obj = Selenium_Run(self.fed_weblink)
        self.driver=selenium_obj.run_Fed_driver_chrome()
        self.filename= "../Scraped_Data/fed_SpeechData.xlsx"
        
        
    def run_fed_scraping(self):
        """
            Method Name: run_fed_scraping
            Description: This method will  auto scraping and update new speeches from FED website and update Scraped_Data/fed_SpeechData.xlsx
            Output: Scraped_Data/fed_SpeechData.xlsx
            On Failure: Exception

            Written By: OBI
            Version: 1.0
            Revisions: None

                                                        """
        try:

            fed_data = pd.read_excel(self.filename)

            fed_data['date'] = pd.to_datetime(fed_data['date'])
            last_date = fed_data['date'][0].date()



            df1 = pd.DataFrame(columns=["date", "link", "speaker", "title"])
            action = ActionChains(self.driver)
            for _ in range(1):
                time.sleep(5)
                date = [i.text for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/div[1]/div/div/time')))]
                #     print(date)
                links = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/div[1]/div/div/p/em/a')))]
                #     print(links)
                speaker_name = [i.text for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/div[1]/div/div/p/em/a')))]
                #     print(title)
                title = [i.text for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/div[1]/div/div/p[3]')))]
                #     print(speaker_name)
                next_page_eles = [i for i in WebDriverWait(self.driver, 7).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/ul[1]/li/a')))]
                time.sleep(5)

                last_page = next_page_eles[-1]
                for date, links, title, speaker_name in zip(date, links, title, speaker_name):
                    df1.loc[len(df1.index)] = [date, links, title, speaker_name]
                action.move_to_element(last_page).click().perform()


            df1['date']=pd.to_datetime(df1['date'])
            df2 = pd.DataFrame()
            for date, link, title, speaker_name in zip(df1['date'], df1['link'], df1['title'], df1['speaker']):
                # print(date.date())
                # print(link)
                if (date > last_date):

                    self.driver.get(link)
                    # print(link)
                    time.sleep(3)

                    try:

                        whl_txt = [i.text for i in WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="article"]/div[3]/p')))]
                        whl_txt = " ".join(whl_txt)


                    except:
                        whl_txt = "na"
                    # print('before',df2.head())

                    df2.loc[len(df2.index), ['date', 'link', 'title', 'speaker', 'WHOLE_TEXT']]=[date.date(),link,title,speaker_name,whl_txt]




                else:
                    print('scraping is upto date in fed_SpeechData.xlsx!!')
                    break
            # print('after', df2.head())
            fed_data['date'] = fed_data['date'].dt.date
            fed_data = pd.concat([df2, fed_data], axis=0, ignore_index=True)


            # Write the DataFrame to the Excel file
            fed_data.to_excel(self.filename,encoding='ascii',index=False)
        except Exception as e:
            print(e)


if __name__=='__main__':
    obj=Fed_Scraping()
    obj.run_fed_scraping()
