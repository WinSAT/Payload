#!/usr/bin/env python3

from app.handlers import command_handler

# RETURN CODES
RETURN_CODE = {
    0 : "OK",
    1 : "ERR"
}

COMMANDS = {
    "ping",
    "get_power_state"
}

PORT_NAME = {
    0 : "/dev/ttyAMA0"
}

REGEX = "\<\<(.*?)\>\>"