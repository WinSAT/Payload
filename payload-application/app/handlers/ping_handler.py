#!/usr/bin/env python3

'''
Class for handling ping command received from OBC
'''

import time
from app.winlogging import logger

class PingHandler:

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("ping-handler")

    def handle_ping(self):
        return "pong"


