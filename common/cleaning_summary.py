


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
            print('cleaning data',data.head())
            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('ul>li>', '<ul><li>'))
            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('/li>li>', '</li><li>'))
            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('/li>/ul>', '</li></ul>'))
            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('./li>', '.</li></ul>'))
            # print('before appending tag in last', data.Summary.iloc[1])
            # FED_Data_wrong_format = data[~data['Summary'].str.endswith('</li></ul>')]
            # print('wrong index',FED_Data_wrong_format.index)
            # data.iloc[FED_Data_wrong_format.index] = data['Summary'] + '</li></ul>'
            # print('after appending tag in last',data.head())

            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('<li>', '<li>"'))
            data['quotes'] = data['quotes'].apply(lambda x: str(x).replace('</li>', '"</li>'))
            print('after appending double quote tag in last', data.head())
            return data
        except Exception as e:
            print(e)


