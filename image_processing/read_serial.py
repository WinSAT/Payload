#!/usr/bin/env python3
import time
import serial

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
