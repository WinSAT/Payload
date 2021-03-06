#!/usr/bin/env python3

from distutils.core import setup
import subprocess, os
import shutil

# install service file
service_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "payload.service")
service_file_dest = "/lib/systemd/system/payload.service"
shutil.copyfile(service_file, service_file_dest)
print("Copied {} to {}".format(service_file, service_file_dest))

# create folder for log files
log_file_directory = "/var/log/app"
if not os.path.exists(log_file_directory):
    os.mkdir(log_file_directory)

# create folder for image files
image_file_directory = "/images/"
if not os.path.exists(image_file_directory):
    os.mkdir(image_file_directory)

setup(
    # Application name:
    name="payload-main-application",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Jon Grebe",
    author_email="grebej@uwindsor.ca",

    # Packages
    packages=["app","app.winlogging","app.handlers","app.winserial","app.winapi"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/payload-main-application_v010/",
    license="LICENSE.txt",
    description="Main application to run on payload module.",
    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "pyserial",
        "xmodem"
    ],

    scripts=['run.py']

)

print("\nPayload application installed. Run the following commands to run the service:")
print("(1) sudo systemctl daemon-reload")
print("(2) sudo systemctl enable payload.service")
print("(3) sudo systemctl start payload.service")