import os

import pandas as pd
from prediction import model_prediction
from cleaning_summary import Prediction_Summary_Cleaning
class Ecb_Summary_Prediction:

    def __init__(self):
        self.filename = './summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'
        self.ecb_scrapedata_path = './Scraped_Data/ECB_SpeechData.csv'
        self.ecb_summarydata_path = './summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'


    def summary_prediction(self):
        self.ecb_summary_data = pd.read_excel(self.ecb_summarydata_path)
        self.ecb_scrape_data = pd.read_csv(self.ecb_scrapedata_path,delimiter='|')
        print('ecb summary data ',self.ecb_summary_data.head())
        print('ecb summary data ', self.ecb_scrape_data.head())

        # self.ecb_summary_data['date'] = pd.to_datetime(self.ecb_summary_data['date'], format='%m/%d/%Y')
        # df.head(10)

        # df
        latest_date = self.ecb_summary_data['date'][0]
        df = self.ecb_scrape_data[self.ecb_scrape_data['date'] > latest_date]

        # df.to_excel('new_data_fed_for_prediction.xlsx', encoding='ascii', index=False)
        print(df.head())
        model_prediction_obj=model_prediction()
        df=model_prediction_obj.prediction(df)
        print(df.head())

        cleaning_obj=Prediction_Summary_Cleaning()
        cleaned_data=cleaning_obj.clean_summary(df)
        print(cleaned_data.head())

        # df.to_excel('prediction_test.xlsx',encoding='ascii',index=False)
        appended_fed_data = pd.concat([cleaned_data, self.ecb_summary_data], ignore_index=True)
        # appended_fed_data.to_excel('test.xlsx',encoding='ascii',index=False)
        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Write the DataFrame to the Excel file
        appended_fed_data.to_excel(self.filename, encoding='ascii', index=False)



Ecb_Summary_Prediction().summary_prediction()