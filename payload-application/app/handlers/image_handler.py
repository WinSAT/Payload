#!/usr/bin/env python3

'''
Class for interacting with images (transfer, read/write, captures, etc.)
'''

import time
from winserial import uart
from winlogging import logger

#############
# Config Data
DELAY = 1
UART_PORT = '/dev/ttyS1'
TIMEOUT = 1

# RETURN CODES FROM PAYLOAD
SUCCESS = "<<00>>"
FAILURE = "<<01>>"

COMMANDS = {
    "ping": "<<ping>>",
    "ImageTransfer": "<<imgcap>>",
    "ImageCapture": "<<imgtra>>"
}
# End Config Data
#############

class ImageHandler:

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("image-handler") 

        # setup UART
        self.UART = uart.uart1

    def transfer_image():
        pass

    def image_capture(self):
        # should send hardware a ping and expect a pong back
        success, errors = self.UART.write(COMMANDS["ImageCapture"])
        # return results
        return success, errors

    def image_transfer(self):
        # should send hardware a ping and expect a pong back
        success, errors = self.UART.write(COMMANDS["ImageTransfer"])

        if success:
            # open stream for image transfer
            return self.UART.readImage()
        else:
            return success, errors