#!/usr/bin/env python3

import argparse

# get arguments
parser = argparse.ArgumentParser()
parser.add_argument('--debug', '-d', dest='debug', action='store_const',
                    const=True, default=False,
                    help='run application in debug mode')
parser.add_argument('--uart', '-u', dest='uart', action='store_const',
                    const=False, default=True,
                    help='run application using real uart port - defaults to mock uart connection')
args = parser.parse_args()

# Start payload application
from app import main
main.run(debug=args.debug, uart=args.uart)