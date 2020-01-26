#! /usr/bin/python3.6
'''
Collects, Formats, and Returns the Collected Data for the Methane Analysis Service.
'''

# System Functions
import os
import netCDF4 as cdf
import numpy as np

# Helper Functions
def getNCs():
    '''
    Get a List of Paths to Every Orbit NetCDF File.

    :return: A List of all the NetCDF Files.
    '''
    for root, dirs, files in os.walk('data/', topdown = True):
        ncList = [os.path.join(root, file) for file in files \
                  if file.endswith('.nc')]
    return ncList

def collectData(config, ncList):
    '''
    Collect the Data Specicied in the Configuration.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :param ncList: A List of All Data NetCDF Files.
    :return: TODO
    '''
    # TODO
    return []

def aggregateDataByDay(data):
    '''
    Aggregate the Collected Data by Day and Create a Model Matrix.

    :param data: The Collected Data to be Aggregated by Day.
    :return: A Model Matrix with Day-Aggregated Data.
    '''
    # TODO
    return []

def cleanData(M):
    '''
    Clean a Model Matrix by Performing Matrix Completion on Missing Elements.

    :param M: The Model Matrix to be Completed.
    :return: A Model Matrix without Missing Values.
    '''
    # TODO
    return []

# Class Function
def getData(config):
    '''
    Get the Collected, Cleaned, and Aggregated TROPOMI Data.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :return: A Cleaned Model Matrix of Relevant Observations and Predictors.
    '''
    # Acquire netCDF Files
    ncList = getNCs()
    if len(ncList) == 0:
        raise ValueError

    # Collect the Data
    collectedData = collectData(config, ncList)

    # Aggregate the Data by Day
    aggregatedData = aggregateDataByDay(collectedData)

    # Clean the Data
    cleanedData = cleanData(aggregatedData)

    # Return the Model Matrix
    return cleanedData
