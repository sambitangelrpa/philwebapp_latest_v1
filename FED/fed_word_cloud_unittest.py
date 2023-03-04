import os
import unittest
import logging
import pandas as pd

from common.word_cloud import Word_cloud_generation
from log_exception.log_exception import Log_Exception

class TestWordCloudGeneration(unittest.TestCase):
    def setUp(self):
        self.bank = 'fed'
        self.path = '../summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'
        self.word_cloud_generation = Word_cloud_generation(self.path, self.bank)
        logfile_obj = Log_Exception()
        self.logger = logfile_obj.save_exception()


    # def tearDown(self):
    #     os.remove('../wordcloud/last_update_date_for_wordcloud.xlsx')
    #     os.remove(f'../wordcloud/{self.word_cloud_generation.folder_dict[self.bank]}/2023-03-01_TestSpeaker1.png')
    #     os.remove(f'../wordcloud/{self.word_cloud_generation.folder_dict[self.bank]}/2023-03-01_TestSpeaker2.png')


    def test_color_func(self):
        word = 'positive'
        color = self.word_cloud_generation.color_func(word)
        self.assertEqual(color, '#4676CC')

        word = 'negative'
        color = self.word_cloud_generation.color_func(word)
        self.assertEqual(color, '#FF8811')

        word = 'neutral'
        color = self.word_cloud_generation.color_func(word)
        self.assertEqual(color, '#D9D9D9')

    def test_word_cloud_run(self):
        self.word_cloud_generation.word_cloud()
        assert True

    def test_word_cloud_file(self):

        self.file1=f'../wordcloud/{self.word_cloud_generation.folder_dict[self.bank]}/2023-02-24_Governor Philip N. Jefferson.png'
        self.file2= f'../wordcloud/{self.word_cloud_generation.folder_dict[self.bank]}/2023-02-16_Governor Lisa D. Cook.png'
        print(self.word_cloud_generation.folder_dict[self.bank])
        self.assertTrue(os.path.isfile(
            self.file1))
        self.assertTrue(os.path.isfile(self.file2))



    def test_word_cloud_key_error(self):
        # Testing if an exception is raised if one or more of the specified keys ("date", "quotes", or "speaker") do not exist in the self.data dictionary
        with self.assertLogs(self.logger, level='ERROR'):
            path = '../test_files/fed_test_key_error.xlsx'
            bank = 'fed'
            word_cloud_generation = Word_cloud_generation(path, bank)
            word_cloud_generation.word_cloud()

    def test_word_cloud_file_not_found_error(self):
        # Testing if an exception is raised if the specified file is not found

        with self.assertLogs(self.logger, level='ERROR'):
            path = 'test_file_not_found_error.xlsx'
            bank = 'fed'
            word_cloud_generation = Word_cloud_generation(path, bank)
            word_cloud_generation.word_cloud()

if __name__ == '__main__':
    unittest.main()