#!/usr/bin/env python3
import time
import serial
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from datetime import datetime

def take_picture():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    # allow the camera to warmup
    time.sleep(0.1)

    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array

    # display the image on screen and wait for a keypress
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)

    # Converting datetime object to string
    dateTime = datetime.now()
    timestamp = dateTime.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    # save image with timestamp
    cv2.imwrite(timestamp + '.png', image)

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
)

print("Reading from serial port...")

while 1:
    x = ser.readline();
    if x != '':
        print(x);
    if x == '1':
        take_picture()
