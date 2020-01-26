#! /usr/bin/python3.6
'''
The TROPOMI Methane Analysis Service.
'''

# System Functions
import sys
import errno
import argparse
import logging
import yaml

# TODO Import the Service Tools
from software.analyze import service
from software.analyze.service import MethaneService
from software.collect import collector

# Create the Description
DESC = '''Starts a Service (or a One-Time Command Line Run) to Allow the Methane Analysis Service to Examine the TROPOMI Data.'''

# Setup the Command Line Interface
parser = argparse.ArgumentParser(description = DESC)
parser.add_argument('--config', '-c',
                    help = 'Path to the Configuration YAML File.')
parser.add_argument('--port', '-p',
                    help = 'The Port Number for the REST Service to Listen On.')
parser.add_argument('--host', '-t',
                    help = 'The Host for the REST Service to Bind On.')
parser.add_argument('--outfile', '-o',
                    type = argparse.FileType('w'),
                    default = sys.stdout,
                    help = 'The Output File with Results. \
                    \nDefaults to Standard Output.')
parser.add_argument('--log', '-l',
                    dest = 'logLevel',
                    choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help = 'The Logging Level for the Service Run.')

def getConfig(args):
    '''
    Returns the Dictionary of Configuration Settings from the YAML Configuration
    File Specified in the Argument Parse.

    :param parser: The CLI Arguments Object from `argparse`.
    :return: A Dictionary Mapping Configuration Settings to their Options.
    '''
    config = {}
    if args.config:
        with open(args.config, 'r') as ymlFile:
            config = yaml.load(ymlFile, yaml.SafeLoader)
            return config
    else:
        print('\nERROR : No Valid Configuration Specified.\n')
        sys.exit(errno.EINVAL)

# Create the Main Method for the Service
if __name__ == '__main__':
    # Get the Parsed CLI Arguments
    args = parser.parse_args()

    # Get the Configuration from the YAML File
    config = getConfig(args)

    # Allow Overrides to the Configuration YAML from the CLI
    if args.logLevel:
        config['logging']['level'] = args.logLevel
    if args.port:
        config['REST']['port'] = args.port
    if args.host:
        config['REST']['host'] = args.host

    # Start the Logging Process
    logging.basicConfig(
        format = '%(asctime)s l.%(lineno)-4d %(name)-15s %(levelname)-8s: \
                  %(message)s',
        level = getattr(logging, config['logging']['level'])
    )

    # Get the Data for the Analysis Service
    try:
        M = collector.getData(config)
    except:
        print('\nERROR : No Data Supplied.\n')
        sys.exit(errno.EINVAL)

    # Activate the Service
    logging.info('Starting Service...')
    service = MethaneService(config)
    service.start()
    logging.info('Done!')
