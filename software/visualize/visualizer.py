#! /usr/bin/python3.6
'''
Create Crafty Visualizations of Methane Analysis Results.
'''

# System Functions
import os
import sys
import errno
import numpy as np
import string
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.io import write_image

def randomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def visualizeAnalytic(analytic, results):
    '''
    Visualize the Results of the Selected Analytic in a Nice Geospatial Plot.

    :param analytic: The Full Name of the Chosen Analytic.
    :param results: The Map of Results from the Chosen Analytic.
    :return: The Saved Visualization Filename to the Web Interface.
    '''
    # If Results are None, Plot a Blank Map
    if results is None:
        fig = go.Figure(data = go.Scattergeo(
                 lon = [-100],
                 lat = [40],
                 text = None,
                 mode = 'markers',
                 marker_color = 1,))
        fig.update_layout(title = 'Anomaly Locations on a US Map',
                          geo_scope = 'usa')

    else:
        # Choose and Visualize the Selected Analytic
        fig = go.Figure(data = go.Scattergeo(
                 lon = [val[0] for val in results.values()],
                 lat = [val[1] for val in results.values()],
                 text = None,
                 mode = 'markers',
                 marker_color = 1,))
        fig.update_layout(title = 'Anomaly Locations on a US Map',
                          geo_scope = 'usa')

    # Setup the Write Destination
    pio.orca.config.executable = '/usr/bin/miniconda3/bin/orca'
    writePath = 'software/analyze/static/images/'

    # Write the Image Out to the Webpage
    imageName = randomString(10) + '.png'
    fig.write_image(os.path.join(writePath + imageName))
    return imageName
