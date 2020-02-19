#!/usr/bin/env python3

from winserial import uart
from winlogging import logger
from winapi import obc
from handlers import command_handler

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
    
            if (OBC.check_command(command)):
                OBC.status(True)
                success, response = ch.handle(command)
                if success:
                    OBC.write(response)
                else:
                    OBC.status(False)
            else:
                OBC.status(False)

        except Exception as e:
            logger.warn("Exception {}:{}".format(type(e).__name__, str(e)))
            # pass to error handler here?
            # error_handler.handle(error)

        finally:
            time.sleep(0.01)
            # kick watchdog here


'''
            # send command to handler in seperate thread
                response = command_hander.handle(UART, message)
                if success:
                    logger.info("Completed command received from OBC: {}".format(message))
                    if not UART.write(response):
                        logger.warn("Error trying to write {} message back to OBC {}:{}".format(return_code, type(e).__name__,str(e)))
                else:
                    logger.warn("Errors handling command received from OBC: {}".format(message))
                    if not UART.write(ERROR):
                        logger.warn("Error trying to write {} message back to OBC {}:{}".format(return_code, type(e).__name__,str(e)))

                    # pass something to error handler here?
                    # error_handler.handle(error)


'''

if __name__ == "__main__":
    run()