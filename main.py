#!/usr/bin/env python3

from winserial import uart
from winlogging import logger
from handlers import command_handler
import time
import argparse
import serial
# from handlers import error_handler

#### CONFIG ####

################

# setup logger
logger = logger.Logger("main")

# return codes 
SUCCESS = "<<OK>>"
FAILURE = "<<ER>>"
INVALID = "<<IN>>"

# setup command handler
command_handler = command_handler.CommandHandler()
#error_handler = error_handler.ErrorHandler()

def main():

    while True:
        try: 
            # setup UART
            UART = uart.uart1

            # get arguments
            parser = argparse.ArgumentParser()
            args = parser.parse_args()

            break 

        except Exception as e:
            logger.error("FATAL ERROR: Unable to open UART port {}:{}. No communication with OBC. Retrying in 10 seconds...".format(type(e).__name__, str(e)))
            # maybe reboot here after a while?
            time.sleep(10)

    # start main system loop
    logger.info("Starting read from UART...")
    while True:
        try:
            success, message = UART.read()

            # check if got nothing
            if not message:
                continue

            # check if command is valid
            if (command_handler.check_command(message)):
                if not UART.write(SUCCESS):
                    logger.warn("Error trying to write {} message back to OBC.".format(SUCCESS))
            else:
                if not UART.write(INVALID):
                    logger.warn("Error trying to write {} message back to OBC.".format(INVALID))   

            # send command to handler
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

        except serial.SerialException as e:
            logger.warn("Exception {}:{}".format(type(e).__name__, str(e)))
            # pass to error handler here?
            # error_handler.handle(error)

        finally:
            time.sleep(1)
            # kick watchdog here

if __name__ == "__main__":
    main()