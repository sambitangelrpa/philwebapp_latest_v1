
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from common.run_selenium import Selenium_Run
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from log_exception.log_exception import Log_Exception
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException


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
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

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
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: :  {self.filename} not found {err} In pdf_link_scrape method Ecb_PDF_Link_scraping.py file.')
        except ValueError as err:
            self.logger.error(f'ValueError: : Format specified in the pd.to_datetime() method does not match the date format in the data In pdf_link_scrape method Ecb_PDF_Link_scraping.py file.')
        except TimeoutException as err:
            self.logger.error(f'TimeoutException: : In pdf_link_scrape method unable to fetch webelement in selenium '
                              f'for European Central Bank in Ecb_PDF_Link_scraping.py. {err}')
        except NoSuchElementException as err:
            self.logger.error(f'NoSuchElementException: : In pdf_link_scrape method unable to fetch webelement in selenium '
                              f'for European Central Bank in Ecb_PDF_Link_scraping.py. {err}')
        except TypeError as err:
            self.logger.error(
                f'TypeError: : The data types of the columns in the DataFrame are not compatible or if there is a type mismatch in the program In pdf_link_scrape method unable to fetch webelement in selenium '
                f'for European Central Bank in Ecb_PDF_Link_scraping.py. {err}')
        except PermissionError as err:
            self.logger.error(f'PermissionError: : Unable to write the DataFrame to the Excel file due to permission error! in Ecb_PDF_Link_scraping.py {err}')
        except pd.errors.MergeError as err:
            self.logger.error(f"An error occurred while merging the DataFrames in summary_prediction method in Ecb_PDF_Link_scraping.py {err}")


if __name__=='__main__':

    obj=Ecb_PDF_Scraping()
    obj.pdf_link_scrape()