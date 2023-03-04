import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from common.run_selenium import Selenium_Run
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException
from log_exception.log_exception import Log_Exception


class Fed_Scraping:
    """
             This class is used to scrape new speeches from the website of the Federal Reserve Bank of the United States,
              and update the previously scraped data in the file fed_SpeechData.xlsx.

             Written By: OBI
             Version: 1.0
             Revisions: None

                     """

    def __init__(self):
        self.fed_weblink = "https://www.federalreserve.gov/newsevents/speeches.htm"
        selenium_obj = Selenium_Run(self.fed_weblink)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        self.filename = "../Scraped_Data/fed_SpeechData.xlsx"


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
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            fed_data = pd.read_excel(self.filename)

            if 'date' not in fed_data.columns:
                self.logger.error("The 'date' column is missing in fed_SpeechData.xlsx dataframe in run_fed_scraping method in Fed_Scraping_Automation file.py ")
            fed_data['date'] = pd.to_datetime(fed_data['date'])

            if len(fed_data['date']) > 0:
                last_date = fed_data['date'][0].date()
            else:
                self.logger.error("No Data in date column in fed_SpeechData.xlsx in Fed_Scraping_Automation file.py ")


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

            df1['date'] = pd.to_datetime(df1['date'])
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

                    df2.loc[len(df2.index), ['date', 'link', 'title', 'speaker', 'WHOLE_TEXT']] = [date.date(), link,
                                                                                                   title, speaker_name,
                                                                                                   whl_txt]




                else:
                    print('scraping is upto date in fed_SpeechData.xlsx!!')
                    break
            # print('after', df2.head())
            fed_data['date'] = fed_data['date'].dt.date
            fed_data = pd.concat([df2, fed_data], axis=0, ignore_index=True)

            # Write the DataFrame to the Excel file
            fed_data.to_excel(self.filename, encoding='ascii', index=False)
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: : In run_fed_scraping {self.filename} not found {err}')
            # raise FileNotFoundError
        except TimeoutException as err:
            self.logger.error(f'TimeoutException: : In run_fed_scraping method unable to fetch webelement in selenim '
                              f'for Federal Reserve Bank. {err}')
            # raise TimeoutException
        except ElementNotInteractableException as err:
            self.logger.error(f'ElementNotInteractableException: : In run_fed_scraping method unable to fetch '
                              f'web element in selenium for Federal Reserve Bank. {err}')


        except KeyError as err:
            self.logger.error(f'KeyError: : In run_fed_scraping method unable to fetch the key {err} as column.')

        except ValueError as err:
            self.logger.error(f'ValueError: :Format specified in the pd.to_datetime() method does not match the date '
                              f'format in the data or There is an invalid value in the DataFrame in run_fed_scraping '
                              f'method '
                              f'while saving the fed_data dataframe to excel: :{err}.')

        except OSError as err:
            self.logger.error(f'OSError: :There is an error while writing the dataframe to the Excel file '
                              f'operation in run_fed_scraping method '
                              f'while saving the fed_data dataframe to excel: :{err}.')

        except PermissionError as err:
            self.logger.error(f'PermissionError: : Unable to write the DataFrame to the Excel file due to permission error! in run_fed_scraping method {err}')
        except pd.errors.MergeError as err:
            print(f"pd.errors.MergeError: An error occurred while merging the DataFrames in summary_prediction method "
                  f"in run_fed_scraping method {err}")




if __name__ == '__main__':
    print(os.getcwd())
    obj = Fed_Scraping()
    obj.run_fed_scraping()