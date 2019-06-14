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

In the script [example.py](example.py) you will see how this is done on an insurance claims dataset
taken from the R package .

In the script [example_housing.py](example_housing.py) this is done again on the Boston housing data.

Run the following:
```
python example_housing.py > output.text
```

Will result in the following

```
|      |   SalePrice |   Lower Quantile |   Upper Quantile |
|------+-------------+------------------+------------------|
| 1410 |      230000 |           214925 |           236528 |
| 1411 |      140000 |           135714 |           157317 |
| 1412 |       90000 |            92508 |           114111 |
| 1413 |      257000 |           243729 |           286935 |
| 1414 |      207000 |           178920 |           214925 |
| 1415 |      175900 |           214925 |           258131 |
| 1416 |      122500 |           114111 |           142915 |
| 1417 |      340000 |           301337 |           358945 |
| 1418 |      124000 |           128513 |           150116 |
| 1419 |      223000 |           200523 |           243729 |
| 1420 |      179900 |           157317 |           178920 |
| 1421 |      127500 |           135714 |           157317 |
| 1422 |      136500 |           135714 |           150116 |
| 1423 |      274970 |           164518 |           207724 |
| 1424 |      144000 |           135714 |           157317 |
| 1425 |      142000 |           135714 |           164518 |
| 1426 |      271000 |           229327 |           272533 |
| 1427 |      140000 |           135714 |           157317 |
| 1428 |      119000 |           106910 |           128513 |
| 1429 |      182900 |           178920 |           207724 |
| 1430 |      192140 |           178920 |           207724 |
| 1431 |      143750 |           121312 |           150116 |
| 1432 |       64500 |           106910 |           121312 |
| 1433 |      186500 |           178920 |           200523 |
| 1434 |      160000 |           157317 |           178920 |
| 1435 |      174000 |           150116 |           193322 |
| 1436 |      120500 |           114111 |           135714 |
| 1437 |      394617 |           344543 |           402151 |
| 1438 |      149700 |           135714 |           157317 |
| 1439 |      197000 |           171719 |           200523 |
| 1440 |      191000 |           178920 |           222126 |
| 1441 |      149300 |           135714 |           157317 |
| 1442 |      310000 |           315739 |           394950 |
| 1443 |      121000 |            92508 |           128513 |
| 1444 |      179600 |           186121 |           207724 |
| 1445 |      129000 |           114111 |           135714 |
| 1446 |      157900 |           142915 |           157317 |
| 1447 |      240000 |           250930 |           286935 |
| 1448 |      112000 |            99709 |           128513 |
| 1449 |       92000 |            85307 |            99709 |
| 1450 |      136000 |           121312 |           142915 |
| 1451 |      287090 |           250930 |           279734 |
| 1452 |      145000 |           135714 |           150116 |
| 1453 |       84500 |           135714 |           157317 |
| 1454 |      185000 |           178920 |           200523 |
| 1455 |      175000 |           171719 |           193322 |
| 1456 |      210000 |           178920 |           229327 |
| 1457 |      266500 |           236528 |           286935 |
| 1458 |      142125 |           128513 |           142915 |
| 1459 |      147500 |           135714 |           164518 |
---

Calibration: Quantile Gap 0.6  Proportion in band:  0.74

```

### Pattern Two

TODO

The file [app.py](app.py) and the contents of the [templates](templates) directory is a python flask 
web application you can use to create a new DataRobot project on a dataset and then apply the calibration.

To run:

```
python app.py
```

Then follow the prompts


