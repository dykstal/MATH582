#! /usr/bin/python3.6
'''
Create Crafty Visualizations of Methane Analysis Results.
'''

# System Functions
# TODOi
import numpy as np
import pandas as pd
import seaborn as sns

# Helper Functions
# TODO

# Visualization Functions
# TODO
def testVisualizer():
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
