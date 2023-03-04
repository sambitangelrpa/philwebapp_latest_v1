
from selenium.webdriver.support import expected_conditions as EC
from common.run_selenium import Selenium_Run
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from log_exception.log_exception import Log_Exception
import requests
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException


class Ecb_Scraping:
    """
                 This is a class definition for web scraping
                 the European Central Bank (ECB) website to download a CSV file from the ECB archive.

                 Written By: OBI
                 Version: 1.0
                 Revisions: None

                 """
    def __init__(self):
        self.ecb_download_link = "https://www.ecb.europa.eu/press/key/html/downloads.en.html"
        selenium_obj = Selenium_Run(self.ecb_download_link)
        self.driver = selenium_obj.run_Fed_driver_chrome()
        # self.filename="./Scraped_Data/"

    def download_csv(self):
        """
                                Method Name: download_csv
                                Description: This method download_csv() downloads the ECB_SpeechData.csv from the ECB Archive.
                                Output: ECB_SpeechData.csv
                                On Failure: Exception

                                Written By: OBI
                                Version: 1.0
                                Revisions: None

                                        """
        try:
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()
            link = [i.get_attribute("href") for i in WebDriverWait(self.driver, 7).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-wrapper"]/main/div[2]/p[3]/a')))]


            with open("../Scraped_Data/ECB_SpeechData.csv", 'wb') as f, \
                    requests.get(link[0], stream=True) as r:
                for line in r.iter_lines():
                    f.write(line + '\n'.encode())
        except OSError as err:
            self.logger.error(f'OSError: : Could not open/read file in download_csv in Ecb_csv_Download.py file {err}')
        except IOError as err:
            self.logger.error(f'IOError: : Could not read file in download_csv method in Ecb_csv_Download.py file {err}')
        except InvalidSelectorException as err:
            self.logger.error(f'InvalidSelectorException: : Unable to locate an element with the xpath expression to Xpath is wrong for download csv '
                              f'path in download_csv method in Ecb_csv_Download.py file {err}')
        except ElementNotInteractableException as err:
            self.logger.error(
                f'InvalidSelectorException: : Unable to locate an element with the xpath expression to Xpath is wrong for download csv '
                f'path in download_csv method in Ecb_csv_Download.py file {err}')




if __name__=='__main__':

    obj=Ecb_Scraping()
    obj.download_csv()