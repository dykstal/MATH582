#! /usr/bin/python3.6
'''
Create Crafty Visualizations of Methane Analysis Results.
'''

# System Functions
import sys
import errno
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.io import write_image

def visualizeAnalytic(analytic, results):
    '''
    Visualize the Results of the Selected Analytic in a Nice Geospatial Plot.

    :param analytic: The Full Name of the Chosen Analytic.
    :param results: The Map of Results from the Chosen Analytic.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # Choose and Visualize the Selected Analytic
    fig = go.Figure(data = go.Scattergeo(
             lon = [val[0] for val in results.values()]
             lat = [val[1] for val in results.values()]
             text = None,
             mode = 'markers',
             marker_color = 1,))
    fig.update_layout(title = 'Anomaly Locations on a US Map',
                      geo_scope = 'usa')
    
    # Setup the Write Destination
    pio.orca.config.executable = '/usr/bin/miniconda3/bin/orca'
    writePath = 'software/analyze/static/images'

    # Write the Image Out to the Webpage
    if analytic == 'Local Outlier Factor':
        fig.write_image(writePath + 'LOF.png')
        return 'LOF.png'
    elif analytic == 'Autoencoder':
        fig.write_image(writePath + 'Autoencoder.png')
        return 'Autoencoder.png'
    elif analytic == 'Isolation Forest':
        fig.write_image(writePath + 'IsoForest.png')
        return 'IsoForest.png'
    else:
        print('The Selected Analytic cannot be Visualized')
        sys.exit(errno.EINVAL)
