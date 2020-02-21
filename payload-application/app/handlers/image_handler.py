#!/usr/bin/env python3

'''
Class for interacting with images (transfer, read/write, captures, etc.)
'''

import os
import time
from datetime import datetime
from app.winserial import uart
from app.winlogging import logger
from app import config

# pi camera stuff
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

class ImageHandler():

    def __init__(self):
        # setup logger
        self.logger = logger.Logger("image-handler") 

    def handle_capture(self):
        # capture image here
        success = self.capture_image()
        if success:
            return success, config.RETURN_CODE[2]
        else:
            return success, config.RETURN_CODE[3]

    def handle_transfer(self, OBC):
        # start image transfer
        success = self.transfer_image(OBC)
        if success:
            return success, config.RETURN_CODE[2]
        else:
            return success, config.RETURN_CODE[3]

    def capture_image(self):
        try:
            # initialize the camera and grab a reference to the raw camera capture
            camera = PiCamera()
            camera.resolution = (config.CAMERA["resolution"]["width"], config.CAMERA["resolution"]["height"])
            rawCapture = PiRGBArray(camera)
            
            # allow the camera to warmup
            time.sleep(0.1)
            
            # grab an image from the camera
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array

            # save image with timestamp
            ts = datetime.now()
            filename = '/images/{}-{}-{}.{}:{}:{}.jpg'.format(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)
            cv2.imwrite(filename, image)

            camera.close()

            self.logger.info("Successful image capture. Image saved at: {}".format(filename))
            return True
        
        except Exception as e:
            self.logger.warn("Unable to capture image: {} | {}".format(type(e).__name__, str(e)))
            return False

    def transfer_image(self, OBC):
        try:
            filename = None
            latest_time = 0
            with os.scandir('/images/') as entries:
                for entry in entries:
                    info = entry.stat()
                    if info.st_mtime > latest_time:
                        filename = entry.name 

            if filename == None:
                return False

            filepath = '/images/{}'.format(filename)
            # open up stream to start image transfer

            success = OBC.send_image(filepath)
            return success

        except Exception as e:
            self.logger.warn("Unable to transfer image name: {} error: {}|{}".format(filename, type(e).__name__, str(e)))
            return False