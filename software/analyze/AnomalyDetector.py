#! /usr/bin/python3.6
'''
Create a Class to Implement and Execute Anomaly Detection Activities.
'''

# System Functions
import numpy as np
import sys
import errno

# Analytic Functions
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest

# Class Declaration
class AnomalyDetector:
    '''
    The Anomaly Detector Uses Several Methods to Detect "Outliers" and
    Other Noteworthy Anomalies in a Time Series that Fall Outside of the
    Robust Statistical Boundaries for a Local Window in that Series.
    '''
    def __init__(self, config, M):
        '''
        The Default Constructor.
        '''
        self.config = config
        self.M = M

    def detectWithLocalOutlierFactor(self):
        '''
        TODO: Write Some Stuff.
        '''
        # Find Model Hyperparameters
        hyperParams = self.config['AnomalyDetector']['LocalOutlierFactorHyperparameters']
        return [(-70.154, 35.506), (-100.937, 40.145), (-101.436, 30.123), (-102.567, 45.546), (-110.426, 51.566)]

    def detectWithIsolationForest(self):
        '''
        TODO: Write Some Stuff.
        '''
        # Find Model Hyperparameters
        hyperParams = self.config['AnomalyDetector']['IsolationForestHyperparameters']
        return [(-70.645, 36.125), (-101.214, 39.045)    , (-102.776, 29.333), (-71.543, 37.546), (-108.236,     41.256)]

    def detectWithAutoencoder(self):
        '''
        TODO: Write Some Stuff.
        '''
        # Find Model Hyperparameters
        hyperParams = self.config['AnomalyDetector']['AutoencoderHyperparameters']
        return [(-100.577, 36.124), (-71.147, 41.111)    , (-99.387, 28.534), (-101.765, 39.685), (-100.012, 27.453)]

    def detectAnomalies(self):
        '''
        Fit the Anomaly Detection Model of Choice to the Data. Return Anomalies as a List
        of Lat/Lon Center Points.

        :return: A 1D Vector of Tuples Storing (lon, lat) Center Points for Anomalies.
        '''
        method = self.config['AnomalyDetector']['method']
        if method == 'Local Outlier Factor':
            anomalies = self.detectWithLocalOutlierFactor()
        elif method == 'Isolation Forest':
            anomalies = self.detectWithIsolationForest()
        elif method == 'Autoencoder':
            anomalies = self.detectWithAutoencoder()
        else:
            print('%s is not a Valid Detection Method.' % method)
            sys.exit(errno.EINVAL)
        results = {}
        for i in range(len(anomalies)):
            results[(i + 1)] = anomalies[i]
