#!/usr/bin/env python3

'''
API for interacting with OBC
'''

import time
import re

from winlogging import logger
from winserial import uart
from app import config

class OBC():

    def __init__(self):
        self.logger = logger.Logger("obc-api")
        self.UART = None
        self.use_uart = None

    # try to establish connection with OBC
    def connect(self, use_uart):
        self.use_uart = use_uart
        if self.use_uart:
            while True:
                try: 
                    self.UART = uart.UART(0) 
                except Exception as e:
                    self.logger.error("FATAL ERROR: Unable to open UART port {}:{}. No communication with OBC. Retrying in 10 seconds...".format(type(e).__name__, str(e)))
                    # maybe reboot here after a while? -> pass to error handler for that?
                    time.sleep(10)
        else:
            self.logger.info("Setup fake connection with OBC for testing.")

    # read from UART serial port
    def read(self):
        if self.use_uart:
            success, message = self.UART.read()
            if success:
                return self.unpack(message)
        else:
            return self.unpack(input("Enter fake serial input:"))

    # check if command is valid
    def check_command(self, command):
        if command in config.COMMANDS:
            return True
        else:
            return False

    def pack(self, message):
        return "<<" + message + ">>"

    def unpack(self, message):
        commands = re.findall(config.REGEX, message)
        if len(commands) != 0:
            return commands[0]
        else:
            return None

    # write respone back to OBC
    def write(self, message):
        if self.use_uart:
            self.UART.write(self.pack(message))
        else:
            print(self.pack(message))

    # write status back to OBC
    def status(self, success):
        if self.use_uart:
            if success:
                self.UART.write(self.pack(config.RETURN_CODE[0]))
            else:
                self.UART.write(self.pack(config.RETURN_CODE[1]))

        else:
            if success:
                print(self.pack(config.RETURN_CODE[0]))
            else:
                print(self.pack(config.RETURN_CODE[1]))