#! /usr/bin/python3.6
'''
The REST Service Entry Point for the Methane Analysis Service.
'''

# System Functions
import os
import logging
import datetime as dt
logger = logging.getLogger(__name__)

# RESTful Framework from Flask
from flask import Flask
from flask import request
from flask import render_template
from flask_restful import Api
from flask_restful import Resource

# WSGI Server Framework from Waitress
from waitress import serve

# Homemade Data Analytics and Visualizations
from software.analyze import analyzer
from software.visualize import visualizer

# Service Classes
class MethaneServiceTester(Resource):
    '''
    A Simple Testing Interface that Connects to the REST Endpoint.
    '''
    def get(self):
        logger.debug('REST Test Called')
        return 'REST Endpoint Test Passed!', 200

class MethaneServiceAnalyzer(Resource):
    '''
    Perform Methane Analysis using the Data Analytics Engine.
    '''
    def __init__(self, M):
        self.M = M

    def post(self):
        results = analyzer.runAnalytic(self.M, analytic, latBox, lonBox)
        visualization = visualizer.visualizeAnalytic(analytic, results)
        logger.info('MethaneServiceAnalyze -> POST \nResults: \n\t%s' % resp)
        return results, 200

class MethaneService(Resource):
    '''
    Main Service for Methane Analysis Web Interfaces.
    '''
    def __init__(self, config, M):
        # Initialize Local Configuration
        self.config = config

        # Initialize Model Matrix
        self.M = M

        # Initialize Web Interfaces
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Enable REST Endpoint
        self.api.add_resource(MethaneServiceTester, '/tropomi/test')
        self.api.add_resource(MethaneServiceAnalyzer, '/tropomi/analyzer')

        # Create Routes for the Web Interfaces
        @self.app.route('/tropomi')
        def index():
            TEMPLATE_NAME = 'main.html'
            return render_template(TEMPLATE_NAME)

        @self.app.route('/tropomi', methods = ['POST'])
        def indexPOST():
            # Extract Entries Supplied to the Webpage
            analytic = request.form['analytic']
            if request.form['minLat'] != '':
                minLat = float(request.form['minLat'])
            else:
                minLat = -90.0
            if request.form['maxLat'] != '':
                maxLat = float(request.form['maxLat'])
            else:
                maxLat = 90.0
            if request.form['minLon'] != '':
                minLon = float(request.form['minLon'])
            else:
                minLon = -180.0
            if request.form['maxLon'] != '':
                maxLon = float(request.form['maxLon'])
            else:
                maxLon = 180.0
            if request.form['startDate'] != '':
                startDate = request.form['startDate']
            else:
                startDate = '2010-01-01'
            if request.form['endDate'] != '':
                endDate = request.form['endDate']
            else:
                endDate = dt.datetime.now().strftime('%Y-%m-%d')
            latBox = (min(minLat, maxLat), max(minLat, maxLat))
            lonBox = (min(minLon, maxLon), max(minLon, maxLon))

            # Perform Data Analysis
            results = analyzer.runAnalytic(self.M, analytic, self.config, latBox, lonBox, startDate, endDate)
            visualization = visualizer.visualizeAnalytic(analytic, results)

            # Make Results Readable on the POST
            for i in range(5):
                try:
                    results[(i + 1)] = str(results[(i + 1)][1]) + ' deg Lat.' + ', ' + str(results[(i + 1)][0]) + ' deg Lon.'
                except:
                    results[(i + 1)] = 'None'

            # Post the Results and Visualizations to the Webpage
            POST_TEMPLATE_NAME = 'mainPOST.html'
            IMAGE_PATH = '../static/images/%s' % visualization
            return render_template(POST_TEMPLATE_NAME,
                                   analytic = analytic,
                                   minLat = ('%.3f' % minLat),
                                   maxLat = ('%.3f' % maxLat),
                                   minLon = ('%.3f' % minLon),
                                   maxLon = ('%.3f' % maxLon),
                                   startDate = startDate,
                                   endDate = endDate,
                                   results = results,
                                   image = IMAGE_PATH)

    # Create the REST Service Controller
    def start(self):
        # Start the REST Service and Block
        if self.config['logging']['level'] == 'DEBUG':
            logger.info('Running as Debug with Flask Server.')
            self.app.run(host = self.config['REST']['host'],
                         port = self.config['REST']['port'],
                         debug = True)
        else:
            logger.info('Running Service with Waitress.')
            serve(self.app,
                  host = self.config['REST']['host'],
                  port = self.config['REST']['port'])

        # Shutdown the Service if an Interrupt Action Occurs
        logging.info('Service Stopped.')

        # Delete All Image Files Generated During this Run
        RELATIVE_PATH = 'software/analyze/static/images'
        for imageName in os.listdir(RELATIVE_PATH):
            os.remove((RELATIVE_PATH + imageName))
