#!/usr/bin/env python3

'''
Class for handling commands received from OBC
'''

import time
from app.winlogging import logger
from app.handlers import image_handler
from app.handlers import ping_handler
import re
from app import config

image_handler = image_handler.ImageHandler()
ping_handler = ping_handler.PingHandler()
#error_handler = error_handler.ErrorHandler()

class CommandHandler():

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("command-handler")

    def handle(self, command, OBC):
        # send the command to the appropriate handler
        
        # command: ping
        if command == "ping":
            success, response = ping_handler.handle_ping()
        
        # command: image_capture
        elif command == "capture_image":
            success, response = image_handler.handle_capture()

        # command: image_transfer
        elif command == "transfer_image":
            success, response = image_handler.handle_transfer(OBC)

        else:
            # should never get here
            self.logger.warn("FATAL: Command {} is in valid commands but doesn't have handler.".format(command))
            success = False
        
        return success, response