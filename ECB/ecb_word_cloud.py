from common.word_cloud import Word_cloud_generation
import pandas as pd
import os
class ecb_word_cloud:
    """
             This is a class named ecb_word_cloud. It has a method named run_ecb_wordcloud.
             The purpose of this class is to generate and save wordcloud images for the new generation of quotes in
             the wordcloud/EcbWordCloud/ directory. .

             Written By: OBI
             Version: 1.0
             Revisions: None

    """

    def run_ecb_wordcloud(self):
        """
            Method Name: run_ecb_wordcloud
            Description: It takes no arguments and its purpose is to generate a word cloud image for the new quotes in
            the ALL_ECB_SPEECH_SUMMARY_DATA.xlsx file. It does this by creating a Word_cloud_generation object with
            the path to the summary data file and the bank set to 'ecb'.

            Output: wordcloud/EcbWordCloud/
            On Failure: Exception

            Written By: OBI
            Version: 1.0
            Revisions: None

                                                        """

        try:

            self.path='../summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'


            wordcloud_obj=Word_cloud_generation(self.path,bank='ecb')
            wordcloud_obj.word_cloud()

        except Exception as e:
            print(e)


if __name__=='__main__':
    obj=ecb_word_cloud()
    obj.run_ecb_wordcloud()