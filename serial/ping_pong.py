#!/usr/bin/env python3

import serial
import time
import argparse

# get port name from arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port_name', type=str, default='/dev/ttyAMA0', help ='string of port name ex/ /dev/ttyAMA0')
args = parser.parse_args()

# serial setup
ser = serial.Serial(
        port=args.port_name,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

time.sleep(1)
ser.close()
ser.open()

def pingHandler():
    while 1:
        buffer = ser.readline()
        if buffer:
            try:
                message = buffer.decode('utf-8')
                print("Got message: ", message)
                if message == 'ping':
                    time.sleep(1)
                    ser.write('pong'.encode('utf-8'))
                    print("Sent back a pong")
            except:
                print('decode fail:', str(buffer))

try:
    pingHandler()
except:
    ser.flush()
    ser.close()
