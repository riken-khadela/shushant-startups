# logger.py

import os
import time

class CustomLogger:
    def __init__(self, log_file_path='/home/user1/startups/shushant-startups/newstartups/log/detail_scraper.py.log'):
        self.log_file_path = log_file_path
        self.setup_logger()

    def setup_logger(self):
        with open(self.log_file_path, 'a'):  # Create the file if it doesn't exist
            pass

    def log(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - INFO - {message}\n"
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_message)

    def error(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - ERROR - {message}\n"
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_message)

    def warning(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - WARNING - {message}\n"
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(log_message)
