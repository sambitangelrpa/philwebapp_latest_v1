import pandas as pd
from common.prediction import model_prediction
from common.cleaning_summary import Prediction_Summary_Cleaning
from log_exception.log_exception import Log_Exception


class boe_Summary_Prediction:
    """
                     This is a Python class called boe_Summary_Prediction. It is designed to predict quotes from speech contents in the summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx file.
                     The class has three instance variables: filename, boe_scrapedata_path, and boe_summarydata_path.
                     These variables are set to file paths for the ALL_BOE_SPEECH_SUMMARY_DATA.xlsx, BOE_SpeechData.xlsx, and ALL_BOE_SPEECH_SUMMARY_DATA.xlsx files, respectively.

                     Written By: OBI
                     Version: 1.0
                     Revisions: None

                             """

    def __init__(self):
        self.filename='../summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx'
        self.boe_scrapedata_path='../Scraped_Data/BOE_SpeechData.xlsx'
        self.boe_summarydata_path='../summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx'


    def summary_prediction(self):
        """
                   Method Name: summary_prediction
                   Description: The summary_prediction method is a function that updates new quote predictions in the "summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx" file. It reads data from the "boe_summarydata_path" and "boe_scrapedata_path" Excel files and extracts the latest data from the scraped data. It uses a machine learning model to predict the quotes and then cleans the data before appending it to the summary file.
                   Output:  summary_prediction/ALL_BOE_SPEECH_SUMMARY_DATA.xlsx
                   On Failure: Exception

                   Written By: OBI
                   Version: 1.0
                   Revisions: None

                                                               """
        try:
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            self.boe_summary_data= pd.read_excel(self.boe_summarydata_path)
            self.boe_scrape_data = pd.read_excel(self.boe_scrapedata_path)

            if 'date' not in self.boe_summary_data.columns:
                self.logger.error("The 'date' column is missing in boe_summary_data dataframe in summary_prediction "
                                  "method in Boe_summary_prediction file.py ")
            if 'date' not in self.boe_scrape_data.columns:
                self.logger.error("The 'date' column is missing in boe_scrape_data dataframe in summary_prediction "
                                  "method in Boe_summary_prediction file.py ")

            if len(self.boe_summary_data['date']) > 0:
                latest_date = self.boe_summary_data['date'][0]
            else:
                self.logger.error("No value in date column in the ALL_BOE_SPEECH_SUMMARY_DATA.xlsx file")

            if self.boe_scrape_data.shape[0] > 0:

                df = self.boe_scrape_data[self.boe_scrape_data['date'] > latest_date]
            else:
                self.logger.error("No data in BOE_SpeechData.xlsx file")

            if df.shape[0] > 0:


                model_prediction_obj=model_prediction()
                print('what we are sending to the model..',df.columns)
                df=model_prediction_obj.prediction(df)
                print('what we are giving to clean after prediction',df.columns)

                cleaning_obj=Prediction_Summary_Cleaning()
                cleaned_data=cleaning_obj.clean_summary(df)
                print('cleaned data>>>>>',cleaned_data)

                appended_boe_data = pd.concat([cleaned_data, self.boe_summary_data], ignore_index=True)

                # Write the DataFrame to the Excel file
                appended_boe_data.to_excel(self.filename,encoding='ascii',index=False)
            else:
                print('ALL_BOE_SPEECH_SUMMARY_DATA.xlsx sheet is upto date!!')
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: : {self.filename} not found in summary_prediction in Ecb_summary_prediction.py {err}')
        except ValueError as err:
            self.logger.error(f'ValueError: : Unable to convert the date strings  to a datetime format in summary_prediction method in Boe_summary_prediction file.py {err}')
        except pd.errors.MergeError as err:
            self.logger.error(f"pd.errors.MergeError: :An error occurred while merging the DataFrames in summary_prediction method in Boe_summary_prediction file.py  {err}")
        except PermissionError as err:
            self.logger.error(f'PermissionError: : Unable to write the DataFrame to the Excel file due to permission error! in summary_prediction method in Boe_summary_prediction file.py {err}')

if __name__=='__main__':
    obj=boe_Summary_Prediction()
    obj.summary_prediction()

