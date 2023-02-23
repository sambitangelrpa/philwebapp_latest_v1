import os

import pandas as pd
from common.prediction import model_prediction
from common.cleaning_summary import Prediction_Summary_Cleaning
class Fed_Summary_Prediction:
    """
                         This class Fed_Summary_Prediction contains a method summary_prediction that
                         updates quote predictions from speech contents in a given excel file ALL_FED_SPEECH_SUMMARY_DATA.xlsx

                         Written By: OBI
                         Version: 1.0
                         Revisions: None

                         """

    def __init__(self):
        self.filename='../summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'
        self.fed_scrapedata_path='../Scraped_Data/fed_SpeechData.xlsx'
        self.fed_summarydata_path='../summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx'


    def summary_prediction(self):
        """
                           Method Name: summary_prediction
                           Description: The summary_prediction method is defined in the Fed_Summary_Prediction class.
                                        It is used to update all new Quote Predictions in the summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx file
                           Output:  summary_prediction/ALL_FED_SPEECH_SUMMARY_DATA.xlsx
                           On Failure: Exception

                           Written By: OBI
                           Version: 1.0
                           Revisions: None

                                                       """
        try:

            self.fed_summary_data= pd.read_excel(self.fed_summarydata_path)
            self.fed_scrape_data = pd.read_excel(self.fed_scrapedata_path)


            self.fed_summary_data['date'] = pd.to_datetime(self.fed_summary_data['date'], format='%m/%d/%Y')
            # df.head(10)


            # df
            latest_date = self.fed_summary_data['date'][0]
            df = self.fed_scrape_data[self.fed_scrape_data['date'] > latest_date]

            # df.to_excel('new_data_fed_for_prediction.xlsx', encoding='ascii', index=False)
            # print(df.head())
            model_prediction_obj=model_prediction()
            print('what we are sending to the model..',df.columns)
            df=model_prediction_obj.prediction(df)
            print('what we are giving to clean after prediction',df.columns)

            cleaning_obj=Prediction_Summary_Cleaning()
            cleaned_data=cleaning_obj.clean_summary(df)
            print('cleaned data>>>>>',cleaned_data)


            # df.to_excel('prediction_test.xlsx',encoding='ascii',index=False)
            appended_fed_data = pd.concat([cleaned_data, self.fed_summary_data], ignore_index=True)
            # appended_fed_data.to_excel('test.xlsx',encoding='ascii',index=False)


            # Write the DataFrame to the Excel file
            appended_fed_data.to_excel(self.filename,encoding='ascii',index=False)
        except Exception as e:
            print(e)


if __name__=='__main__':
    Fed_Summary_Prediction().summary_prediction()



