from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from wordcloud import  WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os
from log_exception.log_exception import Log_Exception

class Word_cloud_generation:
    """
             The Word_cloud_generation class is used to generate word clouds for respective banks and store them in their respective folders. The class takes the path to an Excel file and the name of the bank as input. The Excel file contains data that includes the date, quotes, and speaker
             Written By: OBI
             Version: 1.0
             Revisions: None

                                     """
    def __init__(self,path,bank):

        self.path = path

        self.bank = bank
        self.bank_dict = {'fed':0,'ecb':1,'boe':2}
        self.folder_dict = {'fed':'FedWordCloud','ecb':'EcbWordCloud','boe':'BoeWordCloud'}
        self.last_date_for_word_cloud_filepath = '../wordcloud/last_update_date_for_wordcloud.xlsx'



    def color_func(self,word, *args, **kwargs):
        """
        Method Name: color_func
        Description: This method is used to define color based on the sentiment of the keyword in wordcloud.

        Output: color
        On Failure: Exception

        Written By: OBI
        Version: 1.0
        Revisions: None

        """

        try:

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
        except Exception as e:
            print(e)
    def word_cloud(self):
        """
        Method Name: word_cloud
        Description: This method is used to generate wordcloud from the Quotes prediction and save the png files.

        Output: /wordcloud/
        On Failure: Exception

        Written By: OBI
        Version: 1.0
        Revisions: None

                                         """
        try:
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            self.data = pd.read_excel(self.path)
            self.data['date'] = self.data['date'].dt.date
            self.last_date_data = pd.read_excel(self.last_date_for_word_cloud_filepath)

            self.last_date_update_data = pd.read_excel(self.path)

            if 'date' not in self.last_date_data.columns:
                self.logger.error("The 'date' column is missing in last_date_update_data dataframe in word_cloud method in word_cloud.py file")
            self.last_date = self.last_date_data.date.iloc[self.bank_dict[self.bank]]
            self.last_date_to_update = self.last_date_update_data['date'].iloc[0]
            # print(self.last_date_to_update)

            stopwords = set(STOPWORDS)

            for date,summary,speaker in zip(self.data['date'],self.data['quotes'],self.data['speaker']):
                if date > self.last_date:


                    # text = "".join(review for review in self.data.Summary.iloc[i])
                    # print(text)

                    try:

                        # Generate the image
                        wordcloud = WordCloud(font_path='./arial.ttf', stopwords=stopwords, color_func=self.color_func,
                                              background_color="black", max_words=100, max_font_size=60, min_word_length=5,
                                              width=1080, height=607, colormap='Dark2').generate(summary)
                    except TypeError as err:
                        self.logger.error(f'TypeError: This error due to nan value in quotes column due to which it could not generate wordcloud!{err}')
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

                    wordcloud.to_file(f"../wordcloud/{self.folder_dict[self.bank]}/{date}{'_' + speaker}.png")
                else:
                    break

            self.last_date_data.loc[self.bank_dict[self.bank], 'date'] = self.last_date_to_update



            # Write the DataFrame to the Excel file
            self.last_date_data.to_excel(self.last_date_for_word_cloud_filepath, encoding='ascii', index=False)
        except FileNotFoundError  as err:
            self.logger.error(f'FileNotFoundError: : Unable find file to read in word_cloud method in word_cloud.py {err}')

        except KeyError as err:
            self.logger.error(f'KeyError: :  one or more of the specified keys ("date", "quotes", or "speaker") do not exist in the self.data dictionary in word_cloud method in word_cloud.py {err}')

        except ValueError as err:
            self.logger.error(f'ValueError: : An error occurred when creating the word cloud in word_cloud method in word_cloud.py {err}')

