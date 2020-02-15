#!/usr/bin/env python3

'''
Class for handling ping command received from OBC
'''

import time
from winlogging import logger

class PingHandler:

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("ping-handler")

    def handle(self, uart, buffer):
        return True

