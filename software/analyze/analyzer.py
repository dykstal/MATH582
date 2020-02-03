#! /usr/bin/python3.6
'''
Implement the Methane Analytic Engine.
'''

# System Functions
import sys
from software.analyze.AnomalyDetector import AnomalyDetector

# Helper Functions
def chooseAnalytic(analytic):
    '''
    Routes the Analytic Run toward the Selected Feature.

    :param analytic: The String Name of the Full Analytic.
    :return: True for the Anomaly Detector, False for the Relevance Estimator.
    '''
    if analytic == 'FaST Anomaly Detector':
        return True
    elif analytic == 'Relevance Estimator 9000':
        return False
    else:
        sys.exit('\nError : No Valid Analytic Selected.\n')

def enforceBoundingBox(M, latBox, lonBox):
    '''
    Removes Records from the Data Matrix that Fall Outside the Lat/Lon
    Bounding Box.

    :param M: The Data Matrix.
    :param latBox: The Bounding Latitudes.
    :param lonBox: The Bounding Longitudes.
    :return: The Data Matrix with Only Data Inside the Bounding Box.
    '''
    # TODO
    return M

# Analytic Functions
def runFaSTAnomalyDetector(M, config):
    '''
    Runs the Anomaly Detector for the Methane Mixing Ratio given
    All Predictors in the Data Matrix.

    :param M: The Data Matrix.
    :param config: The Configuration Map for the Program Run.
    :return: The Results of the Anomaly Detection.
    '''
    A = AnomalyDetector(config['AnomalyDetector']['windowSize'],
                        config['AnomalyDetector']['threshold'])
    anomalies, indexAnomalies, edges = A.detectAnomalies(M[config['model']['response']])
    return {'Test1' : anomalies,
            'Test2' : indexAnomalies,
            'Test3' : edges}

def runRelevanceEstimator9000(M, config):
    '''
    Runs the Relevance Estimator for the Methane Mixing Ratio
    given All Predictors in the Data Matrix.

    :param M: The Data Matrix.
    :param config: The Configuration Map for the Program Run.
    :return: The Results of the Anomaly Detection.
    '''
    # TODO
    return {'Test1' : 'Relevant Indicators will be Found!',
            'Test2' : 'They will be XX% Relevant!',
            'Test3' : 'They will be Most Relevant at Places/Times!'}

def runAnalytic(M, analytic, latBox, lonBox):
    '''
    Runs the Selected Analytic and Returns Valid Results.

    :param M: The Data Matrix.
    :param analytic: The Full Name of the Selected Analytic.
    :param latBox: The Bounding Box for Latitude.
    :param lonBox: The Bounding Box for Longitude.
    :return: Results of the Selected Analytic.
    '''
    # Choose an Analytic and Enforce the Bounding Box
    willUseAnomalyDetector = chooseAnalytic(analytic)
    boundedM = enforceBoundingBox(M, latBox, lonBox)

    # Run the Chosen Analytic with the Bounded Data
    if willUseAnomalyDetector:
        results = runFaSTAnomalyDetector(boundedM, config)
    else:
        results = runRelevanceEstimator9000(boundedM, config)
    return results
