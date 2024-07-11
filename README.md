# Finding Outliers

A python script for processing .csv files which contain stock prices

## Prerequisites

The program was tested on Windows, so the installation steps are only for this platform
In order to run the script you need to have [Python](https://www.python.org/downloads/#GeneratedCaptionsTabForHeroSec) (3.8.10 or later) installed and added to PATH

After python is installed open a command line and run
```console
pip install pandas
```

# Setup

The short version:
Drop the script in the same folder as the folder called `stock_price_data_files` and run it, for example by opening a command line in that folder and running it with python:
```console
python find_outliers.py
```

it will prompt you to enter how many files (maximum) you wish to be processed per directory, type the number in the console and hit Enter

After it runs, it will create a new folder in the root called `outliers_results_[date]_[time]`, containing the results. The results are structured the same as the input folder.
This will also create empty .csv files if no outliers were found in a valid processed file, in order to know that it was indeed processed, which is also logged in the console.
An output .csv file will contain the rows with Price values considered outliers from a random sample of 30 consecutive rows from the original files,
plus three more columns ['Mean of 30 values', 'Price - Mean', '% over threshold']
An outlier is a row with a Price value greater than Mean + 2* Standard_Deviation of the sample.
A tip: Different runs will yield different results because the random nature of the sample

The long version:
The input files should be structured like this:
`[root_folder]/stock_price_data_files/[stock_exchange_name]/[stock_ticker].csv`
which will contain multiple `[stock_exchange_name]` folders and `[stock_ticker].csv` files

A `[stock_ticker].csv` file should have three unnamed columns and an arbitrary number of rows containing
`['Ticker', 'Timestamp', 'Price']` in this order, rows need to be ordered by Timestamp

## Notes
An assumption I made is that the 2nd function which returns the list of outliers also needs to process the results by adding the extra columns
The task took more than 2h because I had to install the necessary programs on my personal computer and also look up python syntax because I haven't used it in a long time
and also because I wanted the script to be robust
A lot of enhancements could be added such as some UI, graph plots, turning the script into an executable, profiling performance
I did not comment every line because I believe good code should be (mostly) self-explanatory, even if this might not be the case for this particular task because of the time limit
