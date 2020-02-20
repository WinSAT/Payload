#!/usr/bin/env python3

'''
Class for interacting with images (transfer, read/write, captures, etc.)
'''

import time
from app.winserial import uart
from app.winlogging import logger

class ImageHandler():

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("image-handler") 

    def handle_capture(self):
        try:
            # capture image here
            success = True
            response = "<<DONE>>"

        except Exception as e:
            # return results
            success = False
            errors = str(e)
            
        return success, errors

    def handle_transfer(self):
        #try:
            # begin image transfer
            #stream = open('image.jpg', 'rb')
            #modem.send(stream)

        if success:
            # open stream for image transfer
            return self.UART.readImage()
        else:
            return success, errors