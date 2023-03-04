import unittest
from BOE.Boe_Scraping_Automation import Boe_Scraping
import pandas as pd
import os
class TestFedScraping(unittest.TestCase):

    def setUp(self):
        self.boe_scraping_obj = Boe_Scraping()




    def test_run_fed_scraping(self):
        self.boe_scraping_obj.run_boe_scraping()
        assert True


    def test_fed_data_columns(self):

        print(os.getcwd())
        boe_data=pd.read_excel('../Scraped_Data/BOE_SpeechData.xlsx')

        self.assertIn('date', boe_data.columns)
        self.assertIn('LINK', boe_data.columns)
        self.assertIn('title', boe_data.columns)
        self.assertIn('speaker', boe_data.columns)
        self.assertIn('summary', boe_data.columns)
        self.assertIn('PDF_LINK', boe_data.columns)
        self.assertIn('WHL_TEXT', boe_data.columns)
    def tearDown(self):
        self.boe_scraping_obj.driver.quit()

if __name__ == '__main__':
    unittest.main()
