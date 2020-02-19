#!/usr/bin/env python3

from distutils.core import setup

setup(
    # Application name:
    name="payload-main-application",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Jon Grebe",
    author_email="grebej@uwindsor.ca",

    # Packages
    packages=["app","app.winlogging"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/payload-main-application_v010/",
    license="LICENSE.txt",
    description="Main application to run on payload module.",
    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],

    scripts=['run.py']

)