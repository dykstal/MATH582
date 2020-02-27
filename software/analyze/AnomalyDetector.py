#! /usr/bin/python3.6
'''
Create a Class to Implement and Execute Anomaly Detection Activities.
'''

# System Functions
import os
import sys
import errno
import json
import numpy as np

# Analytic Functions
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from pyod.models.auto_encoder import AutoEncoder
import matplotlib.pyplot as plt

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
        self.M = {'methane_mixing_ratio_bias_corrected': np.array([1,2,3,4,5]),
                  'latitude': np.array([1,2,3,4,5]),
                  'longitude': np.array([1,2,3,4,5])}
        #self.y = self.M[self.config['model']['response']]
        self.y = np.array([i + 1 for i in range(100)])

    def plotAnomalyScores(self, anomalyScores):
        '''
        Plot a Histogram of Anomaly Scores from the Autoencoder Method. These Scores
        will be Saved to the MATH582/software/analyze/static/images Directory. This
        Plot should be Used as a Reference for Selecting the `anomalyScoreCutoff`
        Hyperparameter for this Method.
        '''
        plt.hist(anomalyScores, bins = 'auto')
        plt.title('Distribution of Autoencoder Anomaly Scores (Higher -> More Unusual)')
        plt.savefig(os.path.join('software/analyze/static/images', 'anomalyScoresPlot.png'))

    def removeCommonData(self, spreadStatistic, threshold):
        '''
        Get Rid of Data within One Standard Deviation of the Mean.

        Return the Reduced Data and the Indices of the Reduced Data in the Original Data.
        '''
        # Calculate the Sample Spread Statistic
        if spreadStatistic == 'IQR':
            ySpread = np.quantile(self.y, 0.75) - np.quantile(self.y, 0.25)
        elif spreadStatistic == 'StandardDeviation':
            ySpread = numpy.std(self.y)
        elif spreadStatistic == 'MAD':
            ySpread = np.mean(np.absolute(self.y - mean(self.y)))
        else:
            print('No Valid Spread Statistic Selected')
            sys.exit(errno.EINVAL)

        # Kill Data that are within 1 `spreadStatistic` of the Mean
        yMean = np.mean(self.y)
        yStar = []
        idxList = []
        for idx in range(self.y.shape[0]):
            if np.abs(self.y[idx] - yMean) >= (threshold * ySpread):
                yStar.append(self.y[idx])
                idxList.append(idx)
        return yStar, idxList

    def detectWithLocalOutlierFactor(self):
        '''
        Apply the Local Outlier Factor.
        '''
        # Find Model Hyperparameters
        hpMap = self.config['AnomalyDetector']['LocalOutlierFactorHyperparameters']

        # Get the Thresholded Response
        yStar, idxList = self.removeCommonData(hpMap['spreadStatistic'], hpMap['threshold'])
        yStar = [[elem] for elem in yStar]

        # Instantiate the Local Outlier Factor
        LOF = LocalOutlierFactor(n_neighbors = hpMap['numNeighbors'],
                                 algorithm = hpMap['algorithm'],
                                 leaf_size = hpMap['leafSize'],
                                 metric = hpMap['metric'],
                                 p = hpMap['p'])

        # Fit and Predict with the Local Outlier Factor
        predictions = LOF.fit_predict(yStar)
        scores = LOF.negative_outlier_factor_

        # Report the Lon/Lat Points Corresponding to the Anomalies
        # in the Order of Decreasing Local Outlier Factor (i.e., the
        # Most Anomalous Points are Shown First)
        anomalyIdxList = [idxList[i] for i in range(len(yStar)) if predictions[i] == -1]
        anomalyLonLatMap = {scores[i]: (self.M['longitude'][idx], self.M['latitude'][idx]) \
                            for idx in anomalyIdxList}
        sortedScores = sorted(scores)
        anomaliesLonLatSorted = [anomalyLonLatMap[sortedScores[i]] for i in range(len(sortedScores)) \
                                 if sortedScores[i] in anomalyLonLatMap]
        return anomaliesLonLatSorted

    def detectWithIsolationForest(self):
        '''
        Apply the Isolation Forest.
        '''
        # Find Model Hyperparameters
        hpMap = self.config['AnomalyDetector']['IsolationForestHyperparameters']

        # Get the Thresholded Response
        yStar, idxList = self.removeCommonData(hpMap['spreadStatistic'], hpMap['threshold'])
        yStar = [[elem] for elem in yStar]

        # Instantiate the Local Outlier Factor
        ISO = IsolationForest(n_estimators = hpMap['numEstimators'],
                              bootstrap = hpMap['bootstrap'])

        # Fit and Predict with the Local Outlier Factor
        predictions = ISO.fit_predict(yStar)
        scores = ISO.decision_function(yStar)

        # Report the Lon/Lat Points Corresponding to the Anomalies
        # in the Order of Decreasing Anomaly Score (i.e., the Most
        # Anomalous Points are Shown First)
        anomalyIdxList = [idxList[i] for i in range(len(yStar)) if predictions[i] == -1]
        anomalyLonLatMap = {scores[i]: (self.M['longitude'][idx], self.M['latitude'][idx]) \
                            for idx in anomalyIdxList}
        sortedScores = sorted(scores)
        anomaliesLonLatSorted = [anomalyLonLatMap[sortedScores[i]] for i in range(len(sortedScores)) \
                                 if sortedScores[i] in anomalyLonLatMap]
        return anomaliesLonLatSorted

    def detectWithAutoencoder(self):
        '''
        Apply the Autoencoder Detection Method.
        '''
        # Find Model Hyperparameters
        hpMap = self.config['AnomalyDetector']['AutoencoderHyperparameters']

        # Create and Fit the Autoencoder Model
        AE = AutoEncoder(hidden_neurons = [1 for i in range(hpMap['depth'])])
        AE.fit(self.y.reshape(-1, 1))

        # Get & Plot Anomaly Scores for the Observations
        anomalyScores = AE.decision_scores_
        self.plotAnomalyScores(anomalyScores)

        # Report the Lon/Lat Points Corresponding to the Anomalies
        # in the Order of Decreasing Anomaly Score (i.e., the Most
        # Anomalous Points are Shown First)
        anomalyIdxList = [self.y[i] for i in range(self.y.shape[0]) \
                          if anomalyScores[i] >= hpMap['anomalyScoreCutoff']]
        anomalyLonLatMap = {anomalyScores[i]: (self.M['longitude'][idx], self.M['latitude'][idx]) \
                            for idx in anomalyIdxList}
        sortedScores = sorted(anomalyScores)
        anomaliesLonLatSorted = [anomalyLonLatMap[sortedScores[i]] for i in range(len(sortedScores)) \
                                 if sortedScores[i] in anomalyLonLatMap]
        return anomaliesLonLatSorted

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
        return results
