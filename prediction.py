from summary_model import SpeechSummaryModel
from transformers import (AdamW,T5ForConditionalGeneration,T5TokenizerFast as T5Tokenizer)

class model_prediction:

    def __init__(self):

        self.MODEL_NAME = 't5-large'
        self.tokenizer = T5Tokenizer.from_pretrained(self.MODEL_NAME)


    def load_model(self):
        print('In load model method')
        self.trained_model = SpeechSummaryModel.load_from_checkpoint(
            './model/best-checkpoint (1).ckpt')
        self.trained_model.freeze()
        return self.trained_model

    def summerize(self,text):
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

    def prediction(self,data):
        print('In prediction method')
        import re
        speech_text_col=data.columns[-1]
        print('last col',speech_text_col)
        print(data.shape)
        print(data.info())
        data[speech_text_col] = data[speech_text_col].apply(lambda x: str(x).replace('\n', ''))  # , regex=True
        data[speech_text_col] = data[speech_text_col].apply(lambda x: str(x).replace('_x000D_', ''))

        try:

            for i in data.index[0:]:
                print("Index :", i)
                text = data.loc[i, speech_text_col]
                data.loc[i, "quotes"] = self.summerize(text)
            # print(data)
            # print(data['Summary'])
            return data
        except Exception as e:
            print(e)
            return data






        # data.to_excel('prediction_test_in_predMethod.xlsx', encoding='ascii', index=False)



