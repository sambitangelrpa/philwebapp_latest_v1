import os

import pandas as pd
from common.prediction import model_prediction
from common.cleaning_summary import Prediction_Summary_Cleaning
from log_exception.log_exception import Log_Exception

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
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            self.ecb_summary_data = pd.read_excel(self.ecb_summarydata_path)
            self.ecb_scrape_data = pd.read_csv(self.ecb_scrapedata_path,delimiter='|')
            self.ecb_scrape_data = self.ecb_scrape_data.dropna(subset=['contents'])

            self.ecb_scrape_data = self.ecb_scrape_data.rename(columns={'speakers': 'speaker'})

            if 'date' not in self.ecb_summary_data.columns:
                self.logger.error("The 'date' column is missing in ecb_summary_data dataframe in summary_prediction method in Ecb_summary_prediction file.py ")
                # raise Exception("The 'date' column is missing in fed_summary_data dataframe.")
            if 'date' not in self.ecb_scrape_data.columns:
                self.logger.error("The 'date' column is missing in ecb_scrape_data dataframe in summary_prediction method in Ecb_summary_prediction file.py ")
                # raise Exception("The 'date' column is missing in fed_scrape_data dataframe.")

            self.ecb_summary_data['date'] = pd.to_datetime(self.ecb_summary_data['date'])
            self.ecb_scrape_data['date'] = pd.to_datetime(self.ecb_scrape_data['date'])


            # df
            if len(self.ecb_summary_data['date']) > 0:
                latest_date = self.ecb_summary_data['date'][0]
            else:
                self.logger.error("No value in date column in the ALL_BOE_SPEECH_SUMMARY_DATA.xlsx file")

            # print('ecb_scrape_data',type(self.ecb_scrape_data['date'][0]))

            if self.ecb_scrape_data.shape[0] > 0:
                df = self.ecb_scrape_data[self.ecb_scrape_data['date'] > latest_date]
            else:
                self.logger.error("No data in ECB_SpeechData.csv file")

            if df.shape[0] > 0:
                model_prediction_obj=model_prediction()
                df=model_prediction_obj.prediction(df)
                cleaning_obj=Prediction_Summary_Cleaning()
                cleaned_data=cleaning_obj.clean_summary(df)
                appended_fed_data = pd.concat([cleaned_data, self.ecb_summary_data], ignore_index=True)
                # Write the DataFrame to the Excel file
                appended_fed_data.to_excel(self.filename, encoding='ascii', index=False)
            else:
                print('ALL_ECB_SPEECH_SUMMARY_DATA .xlsx file is upto date')

        except ValueError as err:
            self.logger.error(f'ValueError: : Unable to convert the date strings in self.ecb_summary_data["date"] or self.ecb_scrape_data["date"] to a datetime format in summary_prediction method in Ecb_summary_prediction file.py {err}')

        except PermissionError as err:
            self.logger.error(f'PermissionError: : Unable to write the DataFrame to the Excel file due to permission error! in summary_prediction method in Ecb_summary_prediction file.py {err}')
        except pd.errors.MergeError as err:
            self.logger.error(f"An error occurred while merging the DataFrames in summary_prediction method in Ecb_summary_prediction file.py  {err}")
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: :  {self.filename} not found in summary_prediction in Ecb_summary_prediction.py {err}')


if __name__=='__main__':

    obj=Ecb_Summary_Prediction()
    obj.summary_prediction()
