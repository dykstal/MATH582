#! /usr/bin/python3.6
'''
Collects, Formats, and Returns the Collected Data for the Methane Analysis Service.
'''

# System Functions
import os
import sys
import glob
import errno
import pdb
import pickle
import json

# Data-Related Functions
import numpy as np
import datetime as dt
from h5py import File
from netCDF4 import Dataset
import rpy2.robjects as R

# Helper Functions
def _dateToTime(dateString):
    '''
    Converts %Y-%m-%d to Seconds since 2010-01-01.

    :param dateString: A Valid Date String.
    :return: The Number of Seconds from that Date to 2010-01-01.
    '''
    dateStringDT = dt.datetime.strptime(dateString, '%Y-%m-%d')
    return (dateStringDT - dt.datetime(2010, 1, 1)).total_seconds()

def applyDateFilter(config, M):
    '''
    Filters Data to Fall between a Start and End Date.

    :param config: The Configuration Dictionary from YAML.
    :param M: The Model Variable Map.
    :return: The Data Map between the Start and End Dates from Configuration.
    '''
    if config['model']['startDate'] is not None and config['model']['endDate'] is not None:
        startTime = _dateToTime(config['model']['startDate'])
        endTime = _dateToTime(config['model']['endDate'])
        indicesToKeep = [i for i in range(M['time'].shape[0]) if i >= startTime and i <= endTime]
        newM = {}
        for key in M:
            if M[key].shape[0] == M['time'].shape[0]:
                newM[key] = np.array([M[key][:][i] for i in indicesToKeep])
            else:
                newM[key] = M[key][:]
        return newM
    else:
        return {key: M[key][:] for key in M}

def getNCs():
    '''
    Get a List of Paths to Every Orbit NetCDF File.

    :return: A List of all the NetCDF Files.
    '''
    filePath = 'data/'
    return [os.path.join(filePath, f) for f in os.listdir(filePath) if f.endswith('.nc')]

def collectData(config, ncList):
    '''
    Collect the Data Specicied in the Configuration.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :param ncList: A List of All Data NetCDF Files.
    :return: A Map of Variable Names to a List of their NetCDF Data Structures.
    '''
    # Find Region Name and Lat/Lon Bounding Box from Configuration
    regionName = config['model']['regionName']
    latLower = config['model']['latLower']
    latUpper = config['model']['latUpper']
    lonLower = config['model']['lonLower']
    lonUpper = config['model']['lonUpper']

    # Get All the Variables we want to Copy, Separated by NetCDF Group
    prodVars = config['model']['prodVars']
    geoVars = config['model']['geoVars']
    detailedVars = config['model']['detailedVars']
    inputVars = config['model']['inputVars']

    # Create a Universal Map of All Variables to Copy
    # Map Variable Names to Empty Collection
    allVars = []
    allVars.extend([(u'PRODUCT/' + v) for v in prodVars])
    allVars.extend([(u'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/' + v) for v in geoVars])
    allVars.extend([(u'PRODUCT/SUPPORT_DATA/DETAILED_RESULTS/' + v) for v in detailedVars])
    allVars.extend([(u'PRODUCT/SUPPORT_DATA/INPUT_DATA/' + v) for v in inputVars])
    varMap = dict.fromkeys([v.split('/')[-1] for v in allVars])
    TO_SKIP = ['PRODUCT/time_utc',
               u'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds',
               u'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds']

    # Create Data Structures for Storing Data in Spatial Order
    for v in varMap.keys():
        varMap[v] = []
    varMap['latLowLeft'] = []
    varMap['lonLowLeft'] = []
    varMap['latLowRight'] = []
    varMap['lonLowRight'] = []
    varMap['latUpRight'] = []
    varMap['lonUpRight'] = []
    varMap['latUpLeft'] = []
    varMap['lonUpLeft'] = []
    areObs = False

    # Find the Values for All Variables
    numDone = 0
    numTotal = len(ncList)
    for fileName in ncList:
        print('Processing %s...' % fileName)
        ncFile = Dataset(fileName, 'r')

        # Get Key Space/Time Information; Pass Over Empty Files
        try:
            lat = ncFile['PRODUCT/latitude'][:].data[0].flatten()
            lon = ncFile['PRODUCT/longitude'][:].data[0].flatten()
            sd = dt.datetime(2010, 1, 1) + dt.timedelta(seconds = int(ncFile['PRODUCT/time'][:].data[0]))
        except KeyError as ke:
            numTotal -= 1
            continue

        # Find Indices of Spatial Locations in the Data (within the Bounding Box)
        # If they Exist, Collect Time-Space Data in Detail
        locInds = np.where((lon > lonLower) * (lon < lonUpper) * (lat > latLower) * (lat < latUpper))[0]
        if len(locInds) > 0:
            areObs = True
            time = []
            for t in ncFile['PRODUCT/delta_time'][:].data[0]:
                # Get the Detailed Time Data (Seconds since 2010-01-01)
                time.extend([(sd + dt.timedelta(seconds = int(t) / 1e3)) \
                             for i in range(ncFile['PRODUCT/latitude'][:].data[0].shape[1])])
            time = np.array(time)

            # Create an H5 File to Store Results more Concisely
            h5Name = 'tropomi_samples_' + regionName + '_' + time[0].strftime('%Y%m%d%H%M%S')
            h5Name += ('_' + time[-1].strftime('%Y%m%d%H%M%S') + '.h5')
            if os.path.exists(h5Name):
                os.remove(h5Name)

            # Get/Add the Detailed Spatial Data
            latStar = ncFile[u'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'][:].data[0]
            lonStar = ncFile[u'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'][:].data[0]
            varMap['latLowLeft'] = latStar[:,:,0].flatten()[locInds]
            varMap['lonLowLeft'] = lonStar[:,:,0].flatten()[locInds]
            varMap['latLowRight'] = latStar[:,:,1].flatten()[locInds]
            varMap['lonLowRight'] = lonStar[:,:,1].flatten()[locInds]
            varMap['latUpRight'] = latStar[:,:,2].flatten()[locInds]
            varMap['lonUpRight'] = lonStar[:,:,2].flatten()[locInds]
            varMap['latUpLeft'] = latStar[:,:,3].flatten()[locInds]
            varMap['lonUpLeft'] = lonStar[:,:,3].flatten()[locInds]

            # Add the Detailed Time Data
            for v in allVars:
                vTrunc = v.split('/')[-1]
                if v == 'PRODUCT/time':
                    varMap[vTrunc].extend(np.array([(t - dt.datetime(2010, 1, 1)).total_seconds() \
                                                    for t in time[locInds]]))
                elif v in TO_SKIP:
                    continue
                else:
                    varMap[vTrunc].extend(ncFile[v][:].data[0].flatten()[locInds])
            numDone += 1
            print('Done [%d/%d]' % (numDone, numTotal))

    # Error Out if no Data was Found
    if not areObs:
        print('Exiting: No Observations Found.')
        sys.exit(errno.EINVAL)

    # Otherwise, Write to the Specified H5 Outfile
    h5FileName = config['model']['h5FileName']
    h5Out = File(os.path.join('data/', h5FileName), 'w')
    for v in allVars:
        if v in TO_SKIP:
            continue
        vTrunc = v.split('/')[-1]
        h5Out.create_dataset(vTrunc, data = varMap[vTrunc][:])
    for corner in ['LowLeft', 'LowRight', 'UpLeft', 'UpRight']:
        for l in ['lat', 'lon']:
            h5Out.create_dataset(l + corner, data = varMap[l + corner][:])
    h5Out.close()

    # Return the Data Map
    M = File(os.path.join('data/', h5FileName), 'r+')
    return M

# Class Functions
def getDataFromNetCDF(config):
    '''
    Get the Collected, Cleaned, and Aggregated TROPOMI Data from NetCDF Files.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :return: A Cleaned Model Matrix of Relevant Observations and Predictors.
    '''
    # Acquire netCDF Files
    ncList = getNCs()
    if len(ncList) == 0:
        raise ValueError

    # Collect the Data
    M = collectData(config, ncList)

    # Apply a Date Filter to the Data
    M = applyDateFilter(config, M)

    # Return the Model Data
    return M

def getDataFromH5(config):
    '''
    Get the Collected, Cleaned, and Aggregated TROPOMI Data from a Preformatted H5 File.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :return: A Cleaned Model Matrix of Relevant Observations and Predictors.
    '''
    # Open the H5 File and Return the Data
    try:
        M = File(os.path.join('data/', config['model']['h5FileName']), 'r+')
    except OSError as fe:
        print('No H5 File Written Yet - Reading from NetCDF')
        M = getDataFromNetCDF(config)

    # Apply a Date Filter to the Data
    M = applyDateFilter(config, M)
    return M

def getDataFromRData(config):
    '''
    Get the Collected, Cleaned, and Aggregated TROPOMI Data from a Preformatted RData File.

    :param config: The Dictionary of Configuration Settings from the YAML.
    :return: A Cleaned Model Matrix of Relevant Observations and Predictors.
    '''
    # Open the RData File and Return the Data
    try:
        R.r['load'](os.path.join('data/', config['model']['RDataFileName']))
        RData = robjects.globalenv[config['model']['RDataFrameName']]
        names = np.array(RData.names)
        values = np.array(R.r[config['model']['RDataFrameName']])
        M = {names[i]: values[i, :] for i in range(names.shape[0])}
    except Exception as fe:
        print('No RData File Resides in the /data Directory')
        sys.exit(errno.EINVAL)

    # Apply a Date Filter to the Data
    M = applyDateFilter(config, M)
    return M
