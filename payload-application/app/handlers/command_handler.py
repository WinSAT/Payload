#!/usr/bin/env python3

'''
Class for handling commands received from OBC
'''

import time
from winlogging import logger
from handlers import image_handler
from handlers import ping_handler
import re
import threading
import queue

image_handler = image_handler.ImageHandler()
ping_handler = ping_handler.PingHandler()
#error_handler = error_handler.ErrorHandler()


'''
class CommandHandler(threading.Thread):

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
'''

class CommandHandler(threading.Thread):

    def __init__(self, uart):
        # setup logger
        self.logger = logger.Logger("command-handler")
        
        # setup UART - THIS SHOULD BE ONLY THREAD READING AND WRITING TO SERIAL PORT
        while True:
            try: 
                # setup UART
                if uart:
                    self.UART = uart.UART(0)
                else:
                    self.UART = uart.mock_UART(0)
                break 

            except Exception as e:
                self.logger.error("FATAL ERROR: Unable to open UART port {}:{}. No communication with OBC. Retrying in 10 seconds...".format(type(e).__name__, str(e)))
                # maybe reboot here after a while?
                # error_handler.handle(reboot)
                time.sleep(10)

        # setup queue for reading in serial commands
        self.queue = Queue()

    def run(self):
        pass
        # main loop for thread
        # read()
        # checksum()
        # checkcommand()
        # handle()

    def read(self):
        # read from serial port using uart class
        buffer = uart.read()

    def checksum():


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




# setup logger
logger = logger.Logger("main")

def run(debug, uart):

    while True:
        # setup connection to OBC
        try: 
            if uart:
                UART = uart.UART(0)
            else:
                UART = uart.mock_UART(0)
            break 
        except Exception as e:
            logger.error("FATAL ERROR: Unable to open UART port {}:{}. No communication with OBC. Retrying in 10 seconds...".format(type(e).__name__, str(e)))
            # maybe reboot here after a while?
            time.sleep(10)

    # initialize command handler
    command_handler = command_handler.CommandHandler()
    
    # start main system loop
    logger.info("Initiated connection with OBC. Waiting for messages...")
    while True:
        try:
            success, message = UART.read()

            # check if got nothing
            if not message:
                continue

            # check if command is valid
            if (command_handler.check_command(message)):
                if not UART.write(SUCCESS):
                    logger.warn("Error trying to write {} message back to OBC.".format(SUCCESS))
            else:
                if not UART.write(INVALID):
                    logger.warn("Error trying to write {} message back to OBC.".format(INVALID))   

            # send command to handler in seperate thread
                response = command_hander.handle(UART, message)
                if success:
                    logger.info("Completed command received from OBC: {}".format(message))
                    if not UART.write(response):
                        logger.warn("Error trying to write {} message back to OBC {}:{}".format(return_code, type(e).__name__,str(e)))
                else:
                    logger.warn("Errors handling command received from OBC: {}".format(message))
                    if not UART.write(ERROR):
                        logger.warn("Error trying to write {} message back to OBC {}:{}".format(return_code, type(e).__name__,str(e)))

                    # pass something to error handler here?
                    # error_handler.handle(error)

        except serial.SerialException as e:
            logger.warn("Exception {}:{}".format(type(e).__name__, str(e)))
            # pass to error handler here?
            # error_handler.handle(error)

        finally:
            time.sleep(1)
            # kick watchdog here
