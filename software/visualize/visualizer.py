#! /usr/bin/python3.6
'''
Create Crafty Visualizations of Methane Analysis Results.
'''

# System Functions
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap

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

def visualizeAnalytic(analytic, results):
    '''
    Visualize the Results of the Selected Analytic in a Nice Geospatial Plot.

    :param analytic: The Full Name of the Chosen Analytic.
    :param results: The Map of Results from the Chosen Analytic.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # Choose and Visualize the Selected Analytic
    imageName = craftKernelImage()

    #fig = plt.figure(figsize=(8, 8))
    #m = Basemap(projection='lcc', resolution=None,
    #                        width=8E6, height=8E6,
    #                        lat_0=45, lon_0=-100,)
    #m.etopo(scale=0.5, alpha=0.5)

    # Map (long, lat) to (x, y) for plotting
    #x, y = m(-100, 100)
    #plt.plot(x, y, 'ok', markersize=5)
    #plt.text(x, y, '  Anomaly 1', fontsize=12)
    #plt.savefig('test.png')
    if analytic == 'Local Outlier Factor':
        return 'LOF.png'
    elif analytic == 'Autoencoder':
        return 'Autoencoder.png'
    elif analytic == 'Isolation Forest':
        return 'IsoForest.png'
    else:
        return 'LOF.png'
