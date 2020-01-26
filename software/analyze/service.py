#! /usr/bin/python3.6
'''
The REST Service Entry Point for the Methane Analysis Service.
'''

# System Functions
import os
import logging
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
    def post(self):
        # TODO - replace this test with actual data analysis & visualization
        results = analyzer.testAnalytic()
        visualization = visualizer.testVisualizer()
        logger.info('MethaneServiceAnalyze -> POST \nResults: \n\t%s' % resp)
        return results, 200

class MethaneService(Resource):
    '''
    Main Service for Methane Analysis Web Interfaces.
    '''
    def __init__(self, config):
        # Initialize Local Configuration
        self.config = config

        # Initialize Web Interfaces
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Enable REST Endpoint
        self.api.add_resource(MethaneServiceTester, '/tropomi/test')
        self.api.add_resource(MethaneServiceAnalyzer, '/tropomi/analyzer')

        # Create Routes for the Web Interfaces
        @self.app.route('/tropomi')
        def index():
            # TODO -> Fix HTML
            TEMPLATE_NAME = 'main.html'
            return render_template(TEMPLATE_NAME)

        @self.app.route('/tropomi', methods = ['POST'])
        def indexPOST():
            # TODO -> Adapt to Fixed HTML
            # Extract Entries Supplied to the Webpage
            title = request.form['title']
            author = request.form['author']
            text = request.form['text']

            # Perform Data Analysis
            # TODO -> Actually Add Configurable Settings on the Webpage
            results = analyzer.testAnalytic()
            visualization = visualizer.testVisualizer()

            # Post the Results and Visualizations to the Webpage
            POST_TEMPLATE_NAME = 'mainPOST.html'
            IMAGE_PATH = '../static/images/%s' % visualization
            return render_template(POST_TEMPLATE_NAME,
                                   title = title,
                                   author = author,
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
