#! /usr/bin/python3.6
'''
Create Crafty Visualizations of Methane Analysis Results.
'''

# System Functions
import sys
import numpy as np
import pandas as pd
import seaborn as sns

# Helper Functions
# TODO - REMOVE ME
def craftKernelImage():
    '''
    Just a Test Image for a Placeholder.
    '''
    # Set the Seaborn Styling
    sns.set(style = 'white')

    # Generate a Random Correlated Bivariate Dataset
    rs = np.random.RandomState(5)
    mean = [0, 0]
    cov = [(1, 0.5), (0.5, 1)]
    x1, x2 = rs.multivariate_normal(mean, cov, 500).T
    x1 = pd.Series(x1, name="$X_1$")
    x2 = pd.Series(x2, name="$X_2$")

    # Show the Joint Distribution using Kernel Density Estimation
    g = sns.jointplot(x1, x2,
                      kind = 'kde',
                      height = 7,
                      space = 0)

    # Save the Figure to be Displayed by the Service
    FIG_NAME = 'test.png'
    g.savefig('software/analyze/static/images/%s' % FIG_NAME)
    return FIG_NAME

def chooseAnalytic(analytic):
    '''
    Routes the Analytic Visualization toward the Selected Feature.

    :param analytic: The String Name of the Full Analytic.
    :return: True for the Anomaly Detector, False for the Relevance Estimator.
    '''
    if analytic == 'FaST Anomaly Detector':
        return True
    elif analytic == 'Relevance Estimator 9000':
        return False
    else:
        sys.exit('\nError : No Valid Analytic Selected.\n')

# Visualization Functions
def visualizeFaSTAnomalyDetector(results):
    '''
    Craft the Visualization of Anomaly Detection Results.

    :param results: The Map of Results from the Anomaly Detector.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # TODO
    return craftKernelImage()

def visualizeRelevanceEstimator9000(results):
    '''
    Craft the Visualization of Relevance Estimation Results.

    :param results: The Map of Results from the Relevance Estimator.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # TODO
    return craftKernelImage()

def visualizeAnalytic(analytic, results):
    '''
    Visualize the Results of the Selected Analytic in a Nice Geospatial Plot.

    :param analytic: The Full Name of the Chosen Analytic.
    :param results: The Map of Results from the Chosen Analytic.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # Choose and Visualize the Selected Analytic
    willVisualizeAnomalyDetector = chooseAnalytic(analytic)
    if willVisualizeAnomalyDetector:
        imageName = visualizeFaSTAnomalyDetector(results)
    else:
        imageName = visualizeRelevanceEstimator9000(results)
    return imageName
