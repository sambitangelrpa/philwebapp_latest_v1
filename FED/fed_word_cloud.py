from common.word_cloud import Word_cloud_generation

class fed_word_cloud:
    """
                 The fed_word_cloud class has a single method named run_fed_wordcloud.
                run_fed_wordcloud is responsible for generating a word cloud of the new quotes predicted in
                summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx and saving it to wordcloud/FedWordCloud folder.

                 Written By: OBI
                 Version: 1.0
                 Revisions: None

    """

    def run_fed_wordcloud(self):
        """
                Method Name: run_fed_wordcloud
                Description: This method will take all new Quote Prediction in summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx and
                save wordcloud .png files for new generation of quotes in wordcloud/FedWordCloud .

                Output: wordcloud/FedWordCloud
                On Failure: Exception

                Written By: OBI
                Version: 1.0
                Revisions: None

                                                                """
        self.path='./summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'
        wordcloud_obj=Word_cloud_generation(self.path,bank='fed')
        wordcloud_obj.word_cloud()


if __name__=='__main__':
    obj=fed_word_cloud()
    obj.run_fed_wordcloud()