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
import warnings

# Import the Service Tools
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
    print('\nInitializing Configuration...')
    if args.config:
        with open(args.config, 'r') as ymlFile:
            config = yaml.load(ymlFile, yaml.SafeLoader)
            print('Done!')
            return config
    else:
        print('Failed.')
        print('ERROR : No Valid Configuration Specified.\n')
        sys.exit(errno.EINVAL)

# Create the Main Method for the Service
if __name__ == '__main__':
    # Supress Warnings
    if not sys.warnoptions:
        warnings.simplefilter('ignore')

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
        if config['model']['readh5File']:
            print('\nLoading Data from H5...')
            M = collector.getDataFromH5(config)
            print('Done!\n')
        elif config['model']['readRDataFile']:
            print('\nLoading Data from RData...')
            M = collector.getDataFromRData(config)
            print('Done!\n')
        else:
            print('\nLoading Data from NetCDF...')
            M = collector.getDataFromNetCDF(config)
            print('Done!\n')
    except Exception as e:
        print('Failed.')
        print(e)
        print('ERROR : No Data Supplied.\n')
        sys.exit(errno.EINVAL)

    # Activate the Service
    logging.info('Starting Service...')
    service = MethaneService(config, M)
    service.start()
    logging.info('Done!')
