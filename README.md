# TROPOMI Methane Analysis Service
This is a project repository presented by Aidan Dykstal for MATH 582 (STATISTICS PRACTICUM) at the Colorado School of Mines. The following sections detail how to run the service enclosed in this repository.

## Prerequisites
- Python 3.6+
- Python 3.6+ Development Tools

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
