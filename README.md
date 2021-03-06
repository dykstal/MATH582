# TROPOMI Methane Analysis Service
*Aidan Dykstal*

**Announcements:** [2020-02-27] The autoencoder implementation for anomaly detection and the PDF document summarizing how to interpret hyperparameters are *available now*!

## Overview
### The Service
This is a project repository for MATH 582 (STATISTICS PRACTICUM) at the Colorado School of Mines. The code within creates a web-interfaced service used for detecting anomalies in tropospheric methane (as detected by the TROPOMI instrument). Three analytics are supported for anomaly detection now:
- Local Outlier Factor
- Isolation Forest
- Autoencoder Neural Network

### Customizing Analytics
Hyperparameters and customization settings can be applied to these analytics and the raw data they apply to by modifying the configuration YAML file `config.yml`. In addition, time and lat/lon windows can be applied on the web interface and in the configuration YAML. See `AnomalyDetectionCode.pdf` in `/docs` for details on hyperparameters and algorithms.

### Data Management
The analytic is compatible with data stored in JSON, netCDF, H5, and RData files. The configuration YAML must be modified to select a data file type to prioritize.

## Quick Start
### Prerequisites
- Python 3.6+.
- Python 3.6+ Development Tools.
- Orca.

For Ubuntu:
```
sudo apt install python3.6-dev
sudo conda install orca
```
For Centos/RHEL:
```
sudo yum install python36-devel
sudo conda install orca
```

### Installing
Clone the repository and install Python requirements:
```
git clone https://github.com/dykstal/MATH582.git
pip install -r requirements.txt
python setup.py install
```

### Running the Service
Start the service via the command line:
```
python tropomi.py -c config.yml
```

To test that the service started:
- Start the service via the command line (as shown above).
- Visit the following URL in a web browser:
```
http://localhost:8000/tropomi/test
```

To visit the web application and run data analytics:
- Start the service via the command line (as shown above). 
- Visit the following URL in a web browser:
```
http://localhost:8000/tropomi
```
Follow the directions on the webpage to run the analytic and see results.

For more options:
```
python tropomi.py --help
```

### Running Unit Tests
Unit tests are managed by `pytest`. Run them with:
```
python -m pytest
```
