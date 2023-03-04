import pandas as pd
from common.prediction import model_prediction
from common.cleaning_summary import Prediction_Summary_Cleaning
from log_exception.log_exception import Log_Exception


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
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            self.fed_summary_data= pd.read_excel(self.fed_summarydata_path)
            self.fed_scrape_data = pd.read_excel(self.fed_scrapedata_path)

            if 'date' not in self.fed_summary_data.columns:
                self.logger.error("The 'date' column is missing in fed_summary_data dataframe in summary_prediction method in Fed_summary_prediction file.py ")
                # raise Exception("The 'date' column is missing in fed_summary_data dataframe.")
            if 'date' not in self.fed_scrape_data.columns:
                self.logger.error("The 'date' column is missing in fed_scrape_data dataframe in summary_prediction method in Fed_summary_prediction file.py ")
                # raise Exception("The 'date' column is missing in fed_scrape_data dataframe.")

            self.fed_summary_data['date'] = pd.to_datetime(self.fed_summary_data['date'], format='%m/%d/%Y')
            # df.head(10)


            if  len(self.fed_summary_data['date']) > 0:
                latest_date = self.fed_summary_data['date'][0]
            else:
                self.logger.error("No value in date column in the ALL_FED_SPEECH_SUMMARY_DATA.xlsx file")
            if self.fed_scrape_data.shape[0] > 0:
                df = self.fed_scrape_data[self.fed_scrape_data['date'] > latest_date]
            else:
                self.logger.error("No data in fed_SpeechData.xlsx file")

            if df.shape[0]>0:

                model_prediction_obj=model_prediction()
                df=model_prediction_obj.prediction(df)
                cleaning_obj=Prediction_Summary_Cleaning()
                cleaned_data=cleaning_obj.clean_summary(df)
                appended_fed_data = pd.concat([cleaned_data, self.fed_summary_data], ignore_index=True)
                appended_fed_data.to_excel(self.filename,encoding='ascii',index=False)
            else:
                print('ALL_FED_SPEECH_SUMMARY_DATA.xlsx is upto date!!')

        except KeyError as err:
            self.logger.error(f'KeyError: : in summary_prediction method in Fed_summary_prediction file.py unable to '
                              f'fetch the key {err} as column.')
        except AttributeError as err:
            self.logger.error(f'AttributeError: :fed_data DataFrame does not have the required attribute, in summary_prediction method '
                              f'in Fed_summary_prediction file.py '
                              f'while saving the fed_data dataframe to excel: :{err}.')
        except ValueError as err:
            self.logger.error(f'ValueError: :There is an invalid value in the DataFrame summary_prediction method in Fed_summary_prediction file.py '
                              f'while saving the fed_data dataframe to excel: :{err}.')
        except TypeError as err:
            self.logger.error(f'TypeError: :The data types of the DataFrame columns are not compatible with the concatenation '
                              f'operation in summary_prediction method in Fed_summary_prediction file.py '
                              f'while saving the fed_data dataframe to excel: :{err}.')
        except OSError as err:
            self.logger.error(f'OSError: :There is an error while writing the dataframe to the Excel file '
                              f'operation in summary_prediction method in Fed_summary_prediction file.py '
                              f'while saving the fed_data dataframe to excel: :{err}.')
        except IOError as err:
            self.logger.error(f'IOError: :there is an I/O error while accessing the file. '
                              f'operation in summary_prediction method in Fed_summary_prediction file.py '
                              f'while saving the fed_data dataframe to excel: :{err}.')
        except PermissionError as err:
            self.logger.error(f'PermissionError: : Unable to write the DataFrame to the Excel file due to permission error! in summary_prediction method in Fed_summary_prediction file.py {err}')
        except pd.errors.MergeError as err:
            print(f"pd.errors.MergeError: :An error occurred while merging the DataFrames in summary_prediction method in Fed_summary_prediction file.py  {err}")
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: :  {self.filename} not found in summary_prediction in Fed_summary_prediction.py {err}')


if __name__=='__main__':
    Fed_Summary_Prediction().summary_prediction()



