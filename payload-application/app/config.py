#!/usr/bin/env python3

from app.handlers import command_handler

# RETURN CODES
RETURN_CODE = {
    0 : "OK",
    1 : "ERR",
    2 : "DONE",
    3 : "FAIL"
}

COMMANDS = {
    "ping",
    "capture_image",
    "transfer_image"
}

PORT_NAME = {
    0 : "/dev/ttyAMA0"
}

REGEX = "\<\<(.*?)\>\>"


CAMERA = {
    "resolution" : {"height": 1200, "width": 1600} 
}

RETRY = 5