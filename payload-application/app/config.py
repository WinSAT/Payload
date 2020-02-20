#!/usr/bin/env python3

from app.handlers import command_handler

# RETURN CODES
RETURN_CODE = {
    0 : "OK",
    1 : "ERR"
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