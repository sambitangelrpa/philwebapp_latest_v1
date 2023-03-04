import unittest
from FED.Fed_Scraping_Automation import Fed_Scraping
import pandas as pd
import os
class TestFedScraping(unittest.TestCase):

    def setUp(self):
        self.fed_scraping_obj = Fed_Scraping()




    def test_run_fed_scraping(self):
        self.fed_scraping_obj.run_fed_scraping()
        assert True


    def test_fed_data_columns(self):

        print(os.getcwd())
        fed_data=pd.read_excel('../Scraped_Data/fed_SpeechData.xlsx')

        self.assertIn('date', fed_data.columns)
        self.assertIn('link', fed_data.columns)
        self.assertIn('speaker', fed_data.columns)
        self.assertIn('title', fed_data.columns)
    def tearDown(self):
        self.fed_scraping_obj.driver.quit()

if __name__ == '__main__':
    unittest.main()
