from common.word_cloud import Word_cloud_generation

class boe_word_cloud:
    """
             This is a class named "boe_word_cloud" that is used to save wordcloud .png files for a new generation of quotes in the "wordcloud/BoeWordCloud/" directory.
             The "run_boe_wordcloud" method of this class reads new quote predictions from "summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx" and
             generates word clouds using the "Word_cloud_generation" class .

             Written By: OBI
             Version: 1.0
             Revisions: None

    """


    def run_boe_wordcloud(self):
        """
            Method Name: run_ecb_wordcloud
            Description: This method will take all new Quote Prediction in summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx and
            save wordcloud .png files for new generation of quotes in wordcloud/EcbWordCloud/ .

            Output: wordcloud/BoeWordCloud/
            On Failure: Exception

            Written By: OBI
            Version: 1.0
            Revisions: None

                                                               """
        try:

            self.path='../summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx'
            wordcloud_obj=Word_cloud_generation(self.path,bank='boe')
            wordcloud_obj.word_cloud()
        except Exception as e:
            print(e)


if __name__=='__main__':
    obj=boe_word_cloud()
    obj.run_boe_wordcloud()