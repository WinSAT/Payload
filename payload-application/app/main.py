#!/usr/bin/env python3

from app.winserial import uart
from app.winlogging import logger
from app.winapi import obc
from app.handlers import command_handler

import time
import serial

# setup logger
logger = logger.Logger("main")

# setup global objects
OBC = obc.OBC()
ch = command_handler.CommandHandler()

def run(debug, uart):

    logger.info("Trying to initiate connection with OBC...")
    OBC.connect(uart) # this will loop until a connection is made

    logger.info("Initiated connection with OBC. Waiting for messages...")
    # start main system loop
    while True:
        try:
            command = OBC.read() 
            if command == None:
                continue

            if (OBC.check_command(command)):
                OBC.status(True)
                success, response = ch.handle(command)
                if success:
                    logger.info("Successful handling command: {}. Sending back reponse: {}".format(command, response))
                    OBC.write(response)
                else:
                    logger.info("Unsuccessful handling command: {}. Sending back error status...".format(command))
                    OBC.status(False)
            else:
                logger.info("Command received is invalid: {}. Sending back error status...".format(command))
                OBC.status(False)

        except Exception as e:
            logger.warn("Exception {}:{}".format(type(e).__name__, str(e)))
            # pass to error handler here?
            # error_handler.handle(error)

        finally:
            time.sleep(0.01)
            # kick watchdog here

if __name__ == "__main__":
    run()