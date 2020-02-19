#!/usr/bin/env python3
import logging

class Logger():

    def __init__(self, logger_name, log_level=logging.DEBUG):
        # setup logging
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        
        # setup log file handler
        fh = logging.FileHandler('{}.log'.format(logger_name))
        fh.setLevel(log_level)
        
        # setup log console hanlder
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # set log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # add log handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)
    
    def debug(self, message):
        self.logger.debug(message)

    def warn(self, message):
        self.logger.warn(message)
    
    def error(self, message):
        self.logger.error(message)