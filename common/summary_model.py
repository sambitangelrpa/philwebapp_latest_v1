import json
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset,DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
# from sklearn.model_selection import train_test_split
import textwrap
from transformers import (AdamW,T5ForConditionalGeneration,T5TokenizerFast as T5Tokenizer)
from tqdm.auto import tqdm


class SpeechSummaryModel(pl.LightningModule):
    """
                    This class SpeechSummaryModel is a PyTorch Lightning module used for training a T5 model for speech summarization.
                    It initializes the T5 model and tokenizer, and defines the forward, training, validation, and testing steps for the LightningModule. It also configures the optimizer used for training the model.
                    Written By: OBI
                    Version: 1.0
                    Revisions: None

                                            """
    def __init__(self):
        super().__init__()
        self.MODEL_NAME = 't5-large'
        self.tokenizer = T5Tokenizer.from_pretrained(self.MODEL_NAME)

        self.model = T5ForConditionalGeneration.from_pretrained(self.MODEL_NAME, return_dict=True)

    def forward(self, input_ids, attention_mask, decoder_attention_mask, labels=None):
        """
                        Method Name: forward
                        Description: This is a method that defines the forward pass of a PyTorch Lightning module named SpeechSummaryModel.
                                     It takes input_ids, attention_mask, decoder_attention_mask, and labels as input and feeds them to the T5ForConditionalGeneration model. It returns the loss and logits output by the model.

                        Output: loss,logits


                        Written By: OBI
                        Version: 1.0
                        Revisions: None

                                                 """
        output = self.model(input_ids,
                            attention_mask=attention_mask,
                            labels=labels,
                            decoder_attention_mask=decoder_attention_mask)
        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
        """
                        Method Name: forward
                        Description: The training_step method is a function in a PyTorch Lightning LightningModule that defines a single step of training on a batch of data.
                                      It takes as input a batch of data and its index and performs forward pass, computes the loss and returns it. Additionally, it logs the training loss and adds a progress bar during training.

                        Output: loss,logits


                        Written By: OBI
                        Version: 1.0
                        Revisions: None

                                                         """
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, output = self.forward(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    decoder_attention_mask=labels_attention_mask,
                                    labels=labels)

        self.log('train_loss', loss, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, output = self.forward(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    decoder_attention_mask=labels_attention_mask,
                                    labels=labels)

        self.log('validation_loss', loss, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        input_ids = batch['text_input_ids']
        attention_mask = batch['text_attention_mask']
        labels = batch['labels']
        labels_attention_mask = batch['labels_attention_mask']

        loss, output = self.forward(input_ids=input_ids,
                                    attention_mask=attention_mask,
                                    decoder_attention_mask=labels_attention_mask,
                                    labels=labels)

        self.log('validation_loss', loss, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=0.0001)