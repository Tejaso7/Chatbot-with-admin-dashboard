import logging
import logging.config
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class LoggerConfig:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir

        # Ensure the log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Get the current date to append to the log file name
        log_filename = os.path.join(self.log_dir, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

        self.LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'level': logging.INFO,
                },
                'file': {
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'formatter': 'standard',
                    'filename': log_filename,
                    'when': 'midnight',  # Rotate at midnight
                    'interval': 1,  # Rotate every day
                    'backupCount': 30,  # Keep 30 days of logs
                    'encoding': 'utf-8',
                },
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['console', 'file'],
                    'level': logging.INFO,
                    'propagate': True
                },
            }
        }

        # Apply the logging configuration
        logging.config.dictConfig(self.LOGGING_CONFIG)

    def get_logger(self, name):
        return logging.getLogger(name)
