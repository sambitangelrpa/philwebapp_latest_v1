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
    def __init__(self):
        super().__init__()
        self.MODEL_NAME = 't5-large'
        self.tokenizer = T5Tokenizer.from_pretrained(self.MODEL_NAME)

        self.model = T5ForConditionalGeneration.from_pretrained(self.MODEL_NAME, return_dict=True)

    def forward(self, input_ids, attention_mask, decoder_attention_mask, labels=None):
        output = self.model(input_ids,
                            attention_mask=attention_mask,
                            labels=labels,
                            decoder_attention_mask=decoder_attention_mask)
        return output.loss, output.logits

    def training_step(self, batch, batch_idx):
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