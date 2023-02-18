from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from wordcloud import  WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os

class Word_cloud_generation:
    def __init__(self,path,bank):
        self.data = pd.read_excel(path)
        print(self.data.info())
        self.data['date'] = self.data['date'].dt.date
        self.bank=bank
        self.bank_dict={'fed':0,'ecb':1,'boe':2}
        self.folder_dict={'fed':'FedWordCloud','ecb':'EcbWordCloud','boe':'BoeWordCloud'}
        self.last_date_for_word_cloud_filepath='./wordcloud/last_update_date_for_wordcloud.xlsx'
        self.last_date_data=pd.read_excel(self.last_date_for_word_cloud_filepath)
        self.last_date=self.last_date_data.date.iloc[self.bank_dict[self.bank]]
        self.last_date_update_data=pd.read_excel(path)
        self.last_date_to_update=self.last_date_update_data['date'].iloc[0]



    def color_func(self,word, *args, **kwargs):
        # print(word)

        obj = SentimentIntensityAnalyzer()
        sentence = word
        sentiment_dict = obj.polarity_scores(sentence)
        sentiment_dict_out = dict(list(sentiment_dict.items())[0: 3])
        # print(out)
        sentiment = max(sentiment_dict_out, key=sentiment_dict_out.get)
        if sentiment == 'pos':
            color = '#4676CC'  # blue
        elif sentiment == 'neg':
            color = '#FF8811'  # orange
        elif sentiment == 'neu':
            color = '#D9D9D9'  # grey
        # print(word,color)

        return color
    def word_cloud(self):
        # obj = SentimentIntensityAnalyzer()
        # sentence = "divine coincidence"
        # sentiment_dict = obj.polarity_scores(sentence)
        # out = dict(list(sentiment_dict.items())[0: 3])
        # print(out)
        # max(out, key=out.get)
        stopwords = set(STOPWORDS)

        for date,summary,speaker in zip(self.data['date'],self.data['quotes'],self.data['speaker']):
            if date>self.last_date:


                # text = "".join(review for review in self.data.Summary.iloc[i])
                # print(text)
                try:

                # Generate the image
                    wordcloud = WordCloud(font_path='./arial.ttf', stopwords=stopwords, color_func=self.color_func,
                                          background_color="black", max_words=100, max_font_size=60, min_word_length=5,
                                          width=1080, height=607, colormap='Dark2').generate(summary)
                except Exception as e:
                    print(e)
                    pass
                # print(len(wordcloud.words_))
                # date = fed_data.date.iloc[i]
                # speaker = fed_data.speaker_name.iloc[i]
                print('speaker name',speaker)
                print('date', date)

                # fig=plt.figure(figsize=(15, 8))
                # plt.imshow(wordcloud, interpolation='bilinear')
                # plt.axis("off")
                # plt.title('Total Reviews Word Clowd')
                # plt.show()

                wordcloud.to_file(f"./wordcloud/{self.folder_dict[self.bank]}/{date}{'_' + speaker}.png")
            else:
                break
        print('last_date_to_update : ',self.last_date_to_update)
        print('last_date_data df',self.last_date_data.loc[0, 'date'])
        self.last_date_data.loc[self.bank_dict[self.bank], 'date'] = self.last_date_to_update

        if os.path.exists(self.last_date_for_word_cloud_filepath):
            os.remove(self.last_date_for_word_cloud_filepath)

        # Write the DataFrame to the Excel file
        self.last_date_data.to_excel(self.last_date_for_word_cloud_filepath, encoding='ascii', index=False)



