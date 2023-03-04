import os
import unittest
import logging
import pandas as pd
from common.prediction import model_prediction
from FED.Fed_summary_prediction import Fed_Summary_Prediction
from log_exception.log_exception import Log_Exception


class TestWordCloudGeneration(unittest.TestCase):
    def setUp(self):

        self.fed_summary_obj = Fed_Summary_Prediction()
        logfile_obj = Log_Exception()
        self.logger = logfile_obj.save_exception()

    #
    def test_summary_prediction(self):
        self.fed_summary_obj.summary_prediction()
        assert True

    def test_ecb_data_columns(self):

        print(os.getcwd())
        fed_data = pd.read_excel('../summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx')

        self.assertIn('date', fed_data.columns)
        self.assertIn('link', fed_data.columns)
        self.assertIn('speaker', fed_data.columns)
        self.assertIn('title', fed_data.columns)
        self.assertIn('WHOLE_TEXT', fed_data.columns)
        self.assertIn('quotes', fed_data.columns)



    def test_file_not_found_error(self):
        # Testing if an exception is raised if the specified file is not found

        with self.assertLogs(self.logger, level='ERROR'):
            self.fed_summary_obj.summary_prediction()



if __name__ == '__main__':
    unittest.main()