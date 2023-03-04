from common.summary_model import SpeechSummaryModel
from transformers import (AdamW,T5ForConditionalGeneration,T5TokenizerFast as T5Tokenizer)
from log_exception.log_exception import Log_Exception
import re

class model_prediction:
    """
         This is a class named model_prediction which is used to load a custom trained model and perform summarization tasks for speech text. The class has three methods: __init__, load_model, summerize, and prediction
         Written By: OBI
         Version: 1.0
         Revisions: None

                                 """

    def __init__(self):

        self.MODEL_NAME = 't5-large'
        self.tokenizer = T5Tokenizer.from_pretrained(self.MODEL_NAME)
        logfile_obj = Log_Exception()
        self.logger = logfile_obj.save_exception()

    def load_model(self):
        """
        Method Name: load_model
        Description: This method is used to load the pre-trained model from the model folder.

        Output: dataframe
        On Failure: Exception

        Written By: OBI
        Version: 1.0
        Revisions: None

                         """
        try:

            print('In load model method')
            self.trained_model = SpeechSummaryModel.load_from_checkpoint(
                '../model/best-checkpoint (1).ckpt')
            self.trained_model.freeze()
            return self.trained_model
        except FileNotFoundError as err:
            self.logger.error(f'FileNotFoundError: :The checkpoint file could not be found in load_model method in '
                              f'prediction.py . Please '
                              f'check the file path {err} ')
        except RuntimeError as err:
            self.logger.error(f'RuntimeError: :An error has occurred while loading the checkpoint file. Please try '
                              f'again load_model method in prediction.py . {err}')
    def summerize(self,text):
        """
                Method Name: summerize
                Description: This method is used to the summerization task after generating encodings and prepare a summerzation

                Output: dataframe
                On Failure: Exception

                Written By: OBI
                Version: 1.0
                Revisions: None

                                 """
        try:

            print('In summerize method')
            text_encoding = self.tokenizer(text, max_length=2500, truncation=True, return_attention_mask=True,
                                      add_special_tokens=True, return_tensors='pt')
            self.trained_model=self.load_model()
            generate_ids = self.trained_model.model.generate(
                input_ids=text_encoding['input_ids'],
                attention_mask=text_encoding['attention_mask'],
                max_length=600,
                num_beams=2,
                repetition_penalty=2.5,
                length_penalty=1.0,
                early_stopping=True
            )
            preds = [self.tokenizer.decode(gen_id, skip_special_tokens=True, clean_up_tokenization_spaces=True) for gen_id in
                     generate_ids]
            return "".join(preds)
        except ValueError as err:
            self.logger.error(f'ValueError: :The text parameter is not a string or is empty ,the input text is '
                              f'invalid. Please '
                              f'provide a valid input in summerize method in prediction.py {err}')
        except RuntimeError as err:
            self.logger.error(f'RuntimeError: :An error has occurred while generating the summary..in summerize method in prediction.py '
                              f' Please try again{err}')

    def prediction(self,data):
        """
                Method Name: prediction
                Description: This method is load the summerize method and do the prediction of the speech text getting from dataframe

                Output: dataframe
                On Failure: Exception

                Written By: OBI
                Version: 1.0
                Revisions: None

                                         """
        try:

            print('In prediction method')

            speech_text_col=data.columns[-1]
            data[speech_text_col] = data[speech_text_col].apply(lambda x: str(x).replace('\n', ''))  # , regex=True
            data[speech_text_col] = data[speech_text_col].apply(lambda x: str(x).replace('_x000D_', ''))



            for i in data.index[0:]:
                print("Index :", i)
                text = data.loc[i, speech_text_col]
                data.loc[i, "quotes"] = self.summerize(text)
            # print(data)
            # print(data['Summary'])
            return data
        except IndexError as err:
            self.logger.error(f'IndexError: :The columns of the data DataFrame are empty, and the code tries to '
                              f'access the last column using the indexing operation in prediction method in '
                              f'prediction.py file {err}')
        except KeyError as err:
            self.logger.error(f'KeyError: :The "speech_text_col" variable does not exist in the data DataFrame, '
                              f'and the code tries to access it using the indexing operation data[speech_text_col] in '
                              f'prediction method in prediction.py file {err}')
        except ValueError as err:
            self.logger.error(f'ValueError: :the "speech_text_col" variable does not contain a valid column name, '
                              f'and the code tries to access it using the indexing operation data[speech_text_col] in '
                              f'prediction method in prediction.py file {err}')





        # data.to_excel('prediction_test_in_predMethod.xlsx', encoding='ascii', index=False)



