#! /usr/bin/python3.6
'''
Implement the Methane Analytic Engine.
'''

# System Functions
import sys
import errno
import numpy as np
from software.analyze.AnomalyDetector import AnomalyDetector

# Helper Functions
def _dateToTime(dateString):
    '''
    Converts %Y-%m-%d to Seconds since 2010-01-01.

    :param dateString: A Valid Date String.
    :return: The Number of Seconds from that Date to 2010-01-01.
    '''
    dateStringDT = dt.datetime.strptime(dateString, '%Y-%m-%d')
    return (dateStringDT - dt.datetime(2010, 1, 1)).total_seconds()

def chooseAnalytic(analytic, config):
    '''
    Routes the Analytic Run toward the Selected Feature.

    :param analytic: The String Name of the Full Analytic.
    :param config: The Configuration Settings.
    :return: Updated Configuration Settings.
    '''
    if analytic == 'Local Outlier Factor':
        config['AnomalyDetector']['method'] = analytic
        return config
    elif analytic == 'Isolation Forest':
        config['AnomalyDetector']['method'] = analytic
        return config
    elif analytic == 'Autoencoder':
        config['AnomalyDetector']['method'] = analytic
        return config
    else:
        print('\nError : No Valid Analytic Selected.\n')
        sys.exit(errno.EINVAL)

def enforceBoundingBox(M, latBox, lonBox):
    '''
    Removes Records from the Data Matrix that Fall Outside the Lat/Lon
    Bounding Box.

    :param M: The Data Matrix.
    :param latBox: The Bounding Latitudes.
    :param lonBox: The Bounding Longitudes.
    :return: The Data Matrix with Only Data Inside the Bounding Box.
    '''
    indicesToKeep = [i for i in range(M['latitude'].shape[0]) \
                     if latBox[0] <= M['latitude'][i] and latBox[1] >= M['latitude'][i] \
                     and lonBox[0] <= M['longitude'][i] and lonBox[1] >= M['longitude'][i]]
    newM = {}
    for key in M:
        if M[key].shape[0] == M['latitude'].shape[0]:
            newM[key] = np.array([M[key][i] for i in indicesToKeep])
        else:
            newM[key] = M[key]
    return newM

def enforceDateFilter(M, startDate, endDate):
    '''
    Filters Data to Fall between a Start and End Date.

    :param config: The Configuration Dictionary from YAML.
    :param M: The Model Variable Map.
    :return: The Data Map between the Start and End Dates from Configuration.
    '''
    try:
        startTime = _dateToTime(startDate)
    except:
        startTime = 0.0
    try:
        endTime = _dateToTime(endDate)
    except:
        endTime = 1e20
    indicesToKeep = [i for i in range(M['time'].shape[0]) if i >= startTime and i <= endTime]
    newM = {}
    for key in M:
        if M[key].shape[0] == M['time'].shape[0]:
            newM[key] = np.array([M[key][:][i] for i in indicesToKeep])
        else:
            newM[key] = M[key][:]
    return newM

def runAnalytic(M, analytic, config, latBox, lonBox, startDate, endDate):
    '''
    Runs the Selected Analytic and Returns Valid Results.

    :param M: The Data Matrix.
    :param analytic: The Full Name of the Selected Analytic.
    :param latBox: The Bounding Box for Latitude.
    :param lonBox: The Bounding Box for Longitude.
    :return: Results of the Selected Analytic.
    '''
    # Choose an Analytic and Enforce the Bounding Box
    if latBox is not None and lonBox is not None:
        M = enforceBoundingBox(M, latBox, lonBox)
    if startDate is not None and endDate is not None:
        M = enforceDateFilter(M, startDate, endDate)
    AD = AnomalyDetector(chooseAnalytic(analytic, config), M)

    # Run the Chosen Analytic with the Bounded Data
    results = AD.detectAnomalies()
    print(results)
    return results
