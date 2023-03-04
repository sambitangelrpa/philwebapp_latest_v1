import unittest
from ECB.Ecb_csv_Download import Ecb_Scraping
import pandas as pd
import os
class TestFedScraping(unittest.TestCase):

    def setUp(self):
        self.ecb_downloadCSV_obj = Ecb_Scraping()




    def test_download_csv(self):
        self.ecb_downloadCSV_obj.download_csv()
        assert True


    def test_ecb_data_columns(self):

        print(os.getcwd())
        ecb_data = pd.read_csv('../Scraped_Data/ECB_SpeechData.csv',delimiter='|')

        self.assertIn('date', ecb_data.columns)
        self.assertIn('subtitle', ecb_data.columns)
        self.assertIn('speakers', ecb_data.columns)
        self.assertIn('title', ecb_data.columns)
        self.assertIn('contents', ecb_data.columns)

    def tearDown(self):
        self.ecb_downloadCSV_obj.driver.quit()

if __name__ == '__main__':
    unittest.main()
