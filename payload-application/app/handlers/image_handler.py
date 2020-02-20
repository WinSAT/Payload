#!/usr/bin/env python3

'''
Class for interacting with images (transfer, read/write, captures, etc.)
'''

import time
from app.winserial import uart
from app.winlogging import logger

class ImageHandler:

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("image-handler") 

        # setup UART
        self.UART = uart.uart1

    def transfer_image():
        pass

    def image_capture(self):
        try:
            # capture image here
            success = True
            errors = []

        except Exception as e:
            # return results
            success = False
            errors = [str(e)]
            
        return success, errors

    def image_transfer(self):
        # should send hardware a ping and expect a pong back
        try:
            # begin image transfer

            
        if success:
            # open stream for image transfer
            return self.UART.readImage()
        else:
            return success, errors