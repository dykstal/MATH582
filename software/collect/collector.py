#! /usr/bin/python3.6
'''
Collects, Formats, and Returns the Collected Data for the Methane Analysis Service.
'''

# System Functions
import os
from datetime import datetime
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
    :return: A Map of Variable Names to a List of their NetCDF Data Structures.
    '''
    modelVariables = config['model']['variables']
    collectedData = {}
    for var in modelVariables:
        variableData = []
        for ncFile in ncList:
            try:
                variableData.append(cdf.Dataset(ncFile).groups['PRODUCT'].variables[var][:])
            except:
                pass
        collectedData[var] = variableData
    return collectedData

def temporallyReshapeData(data):
    '''
    Shape the Data into Continuous Arrays of the Same Size, in Chronological Order.

    :param data: The Collected Data to be Temporally Reshaped.
    :return: A Dictionary Mapping Variable Names to their Temporal Reshapings.
    '''
    # Create Stacked Columns of Raw Data by Taking Row Means
    stackedColMap = {}
    for var in data.keys():
        stackedCol = []
        for vari in data[var]:
            if len(np.shape(vari)) == 3:
                for i in range(np.shape(vari)[1]):
                    stackedCol.append(np.mean(vari[:, i, :]))
            elif len(np.shape(vari)) == 2:
                for value in vari[0][:]:
                    stackedCol.append(value)
        stackedColMap[var] = stackedCol
    return stackedColMap

def aggregateDataByTime(M, config):
    '''
    Aggregate a Model Matrix by Some Unit of Times, for Instance Days.

    :param M: The Model Matrix to be Aggregated by Time.
    :param config: The Configuration Map for the Program Run.
    :return: A Model Matrix Aggregated by the Configured Time Scale.
    '''
    # If a Time-Aggregation Setting is Specified, then Aggregate
    if config['model']['timeAggHours'] and config['model']['timeVariable']:
        # First, Find the Seconds Since 1970
        epochTimes = []
        for time in M[config['model']['timeVariable']]:
            dtObject = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
            epochTimes.append((dtObject - datetime(1970, 1, 1)).total_seconds())
        # Then, Create an Interval Size for Time Aggregations
        intervalSize = 3600.0 * config['model']['timeAggHours']
        leftEpochTimes = [time - min(epochTimes) for time in epochTimes]
        # Create Index Breakpoints at the Rate of the Aggregation Setting
        splitIndices = []
        timeToSplit = intervalSize
        for i in range(len(leftEpochTimes)):
            if leftEpochTimes[i] >= timeToSplit:
                splitIndices.append(i)
                timeToSplit += intervalSize
        # Aggregate the Data between Each Index Breakpoint
        aggM = {}
        nonTimeKeys = [key for key in M.keys() if key != config['model']['timeVariable']]
        for key in nonTimeKeys:
            aggData = []
            aggData.append(np.mean(M[key][0:splitIndices[0]]))
            for i in range(0, len(splitIndices) - 1):
                aggData.append(np.mean(M[key][splitIndices[i]:splitIndices[i + 1]]))
            aggData.append(np.mean(M[key][splitIndices[-1]:]))
            aggM[key] = aggData
        # Add the Time Column Back in with the Start Time of Each Interval
        timeVariable = config['model']['timeVariable']
        aggM[timeVariable] = []
        aggM[timeVariable].append(M[timeVariable][0])
        for i in splitIndices:
            aggM[timeVariable].append(M[timeVariable][i])
        return aggM
    else:
        return M

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
    mapData = temporallyReshapeData(collectedData)

    # Create the Model Matrix
    M = aggregateDataByTime(M, config)

    # Return the Model Matrix
    return M
