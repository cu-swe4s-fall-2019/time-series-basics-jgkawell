# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data.

## Description
This repository contains Python code for reading/writing data from/to `.csv` files. The code is contained within the `data_import` module and includes functions for reading data that is in a date + value format. Also included are functions for searching for data values based on timestamps as well as rounding the timestamps to a given resolution (in minutes). Finally, you can also use this module to fuse data from multiple `.csv` files into a single output file.

## How to use
In order to see this module in action, you can simple call the module as a script and it will execute a demonstration of its capabilities on the data included in this repository. This can be done with the command below:

```
python data_import.py ./smallData tmp.data 5
```

If you wish to see what arguments are available to you, simply run this:

```
python data_import.py -h
```

You can also import this module to use like any other Python package. Simply import it:

```
import data_import
```

Then you can use all of the functionality in your own scripts. The module consists of a class `ImportData` which enables you to import `.csv` files through initializes an object with a file name (or path). Once that is done, you can use the linear search function within the object to search for values based on their timestamp. The attributes of the class consist of the `type` (`str`) as well as the `_time` and `_value` lists of data.

You can also use the `roundTimeArray` function to round the times to a given resolution (in minutes) and it will automatically average or sum the corresponding values to match the new times and return both the times and values to you in a zip. The specific inputs and outputs of this function are shown below:

```
Parameters
----------
obj : the DataImport object
resolution : the resolution (in minutes) to round to

Returns
----------
zip(time, value) : a zip of the rounded times and values
```

Additionally, you may wish to use the `printArray` function to merge and print to a file the data from multiple `.csv` files. The specific inputs and outputs of this function are shown below:

```
Parameters
----------
data_list : a list of zip objects of data (time, value) pairs
annotation_list : a list of strings with column labels for the data value
base_name : the file name you want to print as
key_file : the name from annotation_list you want to align the data on

Returns
----------
Nothing (creates file of output)
```

## Pandas Import
This repository also contains a Pandas implementation of the data import functionality. This is found in the script `pandas_import.py`. You can easily run it from the command line without any arguments since it automatically rounds the data to 5 minute and 15 minute increments and will pull the data from teh `./smallData` directory. After running, you'll have data saved to the `./out` directory with the names `hw_data_5_pandas.csv` and `hw_data_15_pandas.csv`. The command to run it is below:

```
python pandas_import.py
```

## Installation
The project only requires cloning the repository and making sure that you have Python 3 installed.

If you want to use the Pandas implementation, you'll also need the `pandas` package:

```
pip install pandas
```