#!/usr/bin/env python3

'''
Class for handling commands received from OBC
'''

import time
from winlogging import logger
from handlers import image_handler
from handlers import ping_handler
import re
# from handler import error_handler

#### CONFIG ####

REGEX = "\<\<(.*?)\>\>"

image_handler = image_handler.ImageHandler()
ping_handler = ping_handler.PingHandler()
#self.error_handler = error_handler.ErrorHandler()

# available payload commands
COMMANDS = {
    "PING": {"ping"},
    "IMAGE": {"imgcap", "imgtra"}
}

# return codes 
SUCCESS = "OK"
FAILURE = "ER"
INVALID = "IN"

# End Config Data
#############

class CommandHandler:

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("command-handler")

    def check_command(self, buffer):
        command = self.parse(buffer)
        for key in COMMANDS:
            if command in key:
                return True
        return False

    def handle(self, buffer):
        # send the command to the appropriate handler
        if command in COMMANDS["PING"]:
            success, response = ping_handler.handle(command)
        elif command in COMMANDS["IMAGE"]:
            success, response = image_handler.handle(command)
        else:
            # should never get here
            self.logger.warn("FATAL: Got invalid command from OBC: {}. PREVIOUS CHECK FOR THIS FAILED.".format(command))
            success = False
            response = INVALID
        
        response = format(response)
        return success, response

    # gets input from UART buffer, parses it, and returns commands
    def parse(self, buffer):
        commands = re.findall(REGEX, buffer)
        if commands is not None:
            return True, commands
        else:
            return False, None

    # format responses to be send over serial back to OBC
    def format(self, command):
        return "<<" + command + ">>"


