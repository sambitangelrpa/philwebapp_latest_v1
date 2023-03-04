import os
import unittest
import logging
import pandas as pd
from common.prediction import model_prediction
from ECB.Ecb_summary_prediction import Ecb_Summary_Prediction
from log_exception.log_exception import Log_Exception


class TestWordCloudGeneration(unittest.TestCase):
    def setUp(self):

        self.ecb_summary_obj = Ecb_Summary_Prediction()
        logfile_obj = Log_Exception()
        self.logger = logfile_obj.save_exception()

    #
    def test_summary_prediction(self):
        self.ecb_summary_obj.summary_prediction()
        assert True

    def test_ecb_data_columns(self):

        print(os.getcwd())
        ecb_data = pd.read_excel('../summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx')

        self.assertIn('date', ecb_data.columns)
        self.assertIn('subtitle', ecb_data.columns)
        self.assertIn('speaker', ecb_data.columns)
        self.assertIn('title', ecb_data.columns)
        self.assertIn('contents', ecb_data.columns)
        self.assertIn('quotes', ecb_data.columns)



    def test_file_not_found_error(self):
        # Testing if an exception is raised if the specified file is not found

        with self.assertLogs(self.logger, level='ERROR'):
            self.ecb_summary_obj.summary_prediction()



if __name__ == '__main__':
    unittest.main()