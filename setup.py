#! /usr/bin/python3.6
'''
Setup the Methane Analysis as a Service.
'''

# General System Tools
import os
import sys

# Repeated Methods for Setup
from os import path
from setuptools import setup, find_packages

# Create Short Description
description = "The TROPOMI Methane Analysis as a Service."

# Create Long Description
thisDirectory = path.abspath(path.dirname(__file__))
with open(path.join(thisDirectory, 'README.md'), encoding = 'utf-8') as f:
        longDescription = f.read()

# Get Python Package Requirements
def getRequirements():
    reqs = []
    with open('requirements.txt') as fp:
        reqs += fp.readlines()
    reqs = map(str.strip, reqs)
    return reqs

# Initalize Package Setup Upon Pip
# Installation
setup(
    name = 'TROPOMI_SERVICE',
    version = '0.1.0',
    python_requires = '==3.6',
    description = description,
    long_description = longDescription,
    author = 'Aidan Dykstal',
    author_email = 'dykstal@mymail.mines.edu',
    maintainer = 'Aidan Dykstal',
    maintainer_email = 'dykstal@mymail.mines.edu',
    url = 'https://github.com/dykstal/MATH582',
    include_package_data = True,
    install_requires = getRequirements(),
    packages = find_packages(exclude = ('data', 'tests', 'docs'))
)
