import logging
from datetime import date
import os

class Log_Exception:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_exception(self):
        # Set up the file handler


        today = str(date.today())
        log_filename=f'../logfile_{today}/'
        os.makedirs(log_filename,exist_ok=True)
        # print(log_filename)
        file_handler = logging.FileHandler(log_filename+'logfile.log')
        file_handler.setLevel(logging.ERROR)
        # Set up the console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        return self.logger


