import unittest
from ECB.Ecb_PDF_Link_scraping import Ecb_PDF_Scraping
import pandas as pd
import os

class TestFedScraping(unittest.TestCase):

    def setUp(self):
        self.ecb_PDFscraping_obj = Ecb_PDF_Scraping()




    def test_PDF_Scraping(self):
        self.ecb_PDFscraping_obj.pdf_link_scrape()
        assert True


    def test_ecb_PDFdata_columns(self):

        print(os.getcwd())
        ecb_PDFdata = pd.read_excel('../Scraped_Data/ECB_PDF_Link.xlsx')

        self.assertIn('date', ecb_PDFdata.columns)
        self.assertIn('link', ecb_PDFdata.columns)
        self.assertIn('title', ecb_PDFdata.columns)


    def tearDown(self):
        self.ecb_PDFscraping_obj.driver.quit()

if __name__ == '__main__':
    unittest.main()
