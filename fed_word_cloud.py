from word_cloud import Word_cloud_generation

class fed_word_cloud:

    def run_fed_wordcloud(self):
        self.path='./summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'
        wordcloud_obj=Word_cloud_generation(self.path,bank='fed')
        wordcloud_obj.word_cloud()


if __name__=='__main__':
    obj=fed_word_cloud()
    obj.run_fed_wordcloud()