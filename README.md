Quantile Regression Modelling
=============================

This project demonstrates how you can create a DataRobot project to
do quantile regression modelling.

## Dependencies
 
You will need a DataRobot account and access to a dedicated prediction server.

You will also need a bunch of python libraries, including the DataRobot package

```
pip install pandas
pip install datarobot
```

To run the web application you will need a YAML file that authenticates you against your
DataRobot instance when using the DataRobot Python Package. Please 
[follow these guidelines](https://datarobot-public-api-client.readthedocs-hosted.com/en/v2.7.2/setup/configuration.html)
to set up this this configuration file.


## About

The core functions that build and apply the Quantile Regression project can be found in
the file [QuantileRegression.py](QuantileRegression.py)

The functions are used by the example script and the web application discussed below.


## Usage

### Pattern One

In this usage pattern you take a dataset and use a python script to build a model and then score a
subset of the records, or test dataset.

In the script [example.py](example.py) you will see how this is done.


### Pattern Two

TODO

The file [app.py](app.py) and the contents of the [templates](templates) directory is a python flask 
web application you can use to create a new DataRobot project on a dataset and then apply the calibration.

To run:

```
python app.py
```

Then follow the prompts


