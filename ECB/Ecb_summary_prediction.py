import os

import pandas as pd
from common.prediction import model_prediction
from common.cleaning_summary import Prediction_Summary_Cleaning

class Ecb_Summary_Prediction:
    """
                     This class shall be used to generate quote predictions from speech contents in
                      summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx .

                     Written By: OBI
                     Version: 1.0
                     Revisions: None

                """

    def __init__(self):
        self.filename = '../summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'
        self.ecb_scrapedata_path = '../Scraped_Data/ECB_SpeechData.csv'
        self.ecb_summarydata_path = '../summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx'


    def summary_prediction(self):

        """
                    Method Name: summary_prediction
                    Description: The summary_prediction() method is a member function of the Ecb_Summary_Prediction class.
                                 It updates all new quote predictions in summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx file.
                    Output: summary_prediction/ALL_ECB_SPEECH_SUMMARY_DATA .xlsx
                    On Failure: Exception

                    Written By: OBI
                    Version: 1.0
                    Revisions: None

                                                """

        try:

            self.ecb_summary_data = pd.read_excel(self.ecb_summarydata_path)
            self.ecb_scrape_data = pd.read_csv(self.ecb_scrapedata_path,delimiter='|')
            self.ecb_scrape_data = self.ecb_scrape_data.dropna(subset=['contents'])

            self.ecb_scrape_data = self.ecb_scrape_data.rename(columns={'speakers': 'speaker'})
            self.ecb_summary_data['date'] = pd.to_datetime(self.ecb_summary_data['date'])
            self.ecb_scrape_data['date'] = pd.to_datetime(self.ecb_scrape_data['date'])


            # df
            latest_date = self.ecb_summary_data['date'][0]
            print(latest_date,type(latest_date))
            # print('ecb_scrape_data',type(self.ecb_scrape_data['date'][0]))

            df = self.ecb_scrape_data[self.ecb_scrape_data['date'] > latest_date]

            if df.shape[0] != 0:


                model_prediction_obj=model_prediction()
                df=model_prediction_obj.prediction(df)
                # print(df.head())

                cleaning_obj=Prediction_Summary_Cleaning()
                cleaned_data=cleaning_obj.clean_summary(df)
                print(cleaned_data.head())

                # df.to_excel('prediction_test.xlsx',encoding='ascii',index=False)
                appended_fed_data = pd.concat([cleaned_data, self.ecb_summary_data], ignore_index=True)


                # Write the DataFrame to the Excel file
                appended_fed_data.to_excel(self.filename, encoding='ascii', index=False)
            else:
                print('ALL_ECB_SPEECH_SUMMARY_DATA .xlsx file is upto date')

        except Exception as e:
            print(e)



if __name__=='__main__':

    obj=Ecb_Summary_Prediction()
    obj.summary_prediction()
