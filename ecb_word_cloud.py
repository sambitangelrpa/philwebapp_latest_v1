from word_cloud import Word_cloud_generation
import pandas as pd
import os
class ecb_word_cloud:

    def run_ecb_wordcloud(self):
        self.path='./summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'


        wordcloud_obj=Word_cloud_generation(self.path,bank='ecb')
        wordcloud_obj.word_cloud()


if __name__=='__main__':
    obj=ecb_word_cloud()
    obj.run_ecb_wordcloud()