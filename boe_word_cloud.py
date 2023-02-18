from word_cloud import Word_cloud_generation

class boe_word_cloud:

    def run_boe_wordcloud(self):
        self.path='./summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx'
        wordcloud_obj=Word_cloud_generation(self.path,bank='boe')
        wordcloud_obj.word_cloud()


if __name__=='__main__':
    obj=boe_word_cloud()
    obj.run_boe_wordcloud()