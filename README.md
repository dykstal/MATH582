# TROPOMI Methane Analysis Service
*Aidan Dykstal*
This is a project repository for MATH 582 (STATISTICS PRACTICUM) at the Colorado School of Mines. The code within creates a web-interfaced service used for detecting anomalies in tropospheric methane (as detected by the TROPOMI instrument). Three analytics are supported for anomaly detection now:
- Local Outlier Factor
- Isolation Forest
- Autoencoder
Hyperparameters and customization settings can be applied to these analytics and the raw data they apply to by modifying the configuration YAML file `config.yml`.

## Prerequisites
- Python 3.6+.
- Python 3.6+ Development Tools.

For Ubuntu:
```
sudo apt install python3.6-dev
```
For Centos/RHEL:
```
sudo yum install python36-devel
```

### Installing
Make a virtual environment and install Python requirements:
```
python3.6 -m venv tropomi
source tropomi/bin/activate
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
