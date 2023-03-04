
from log_exception.log_exception import Log_Exception

class Prediction_Summary_Cleaning:
    """
                 The Prediction_Summary_Cleaning class is used to clean and format Quote prediction by adding double quotation marks to each quote tag.
                  The clean_summary() method in this class is used for this purpose.


                 Written By: OBI
                 Version: 1.0
                 Revisions: None

                             """

    def clean_summary(self,data):
        """
                Method Name: clean_summary
                Description: This method is used to clean the Quotes prediction and add the double quotes mark in each tags.

                Output: dataframe
                On Failure: Exception

                Written By: OBI
                Version: 1.0
                Revisions: None

                                                         """
        try:
            # print('cleaning data',data.head())
            logfile_obj = Log_Exception()
            self.logger = logfile_obj.save_exception()

            if 'quotes' in data.columns:

                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('ul>li>', '<ul><li>'))
                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('/li>li>', '</li><li>'))
                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('/li>/ul>', '</li></ul>'))
                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('./li>', '.</li></ul>'))
                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('<li>', '<li>"'))
                data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('</li>', '"</li>'))

                return data
            else:
                self.logger.error('The "quotes" column does not exist in the input data in clean_summary method of '
                                  'cleaning_summary.py file ')

        except TypeError as err:
            self.logger.error('the "quotes" column contains non-string values in clean_summary method of '
                              'cleaning_summary.py file ')


