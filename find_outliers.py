import os
import pandas as pd
from random import randrange
import math
from datetime import datetime

def get_n_random_consecutive_datapoints(file_path, n=30):
    """
    Used for getting a sample of n rows from a .csv file
    

    Parameters
    ----------
    file_path : string
        The absolute file path to the .csv file
    n : TYPE, optional
        The number of rows.
        The default is 30.
    
    Returns
    -------
    None if unsuccessful
    
    or
    
    A pandas DataFrame containing a random sample of n consecutive rows from 
    the .csv file
    with columns ['Ticker', 'Timestamp', 'Price']

    """
    if not file_path.endswith('.csv'):
        print(f'Provided file "{file_path}" does not end in .csv')
        return None
        
    if not os.path.exists(file_path):
        print(f'Provided file "{file_path}" does not exist')
        return None
    
    column_names = ['Ticker', 'Timestamp', 'Price']
    try:
        fileDF = pd.read_csv(filepath_or_buffer=file_path, names=column_names)
    except:
        print(f'Invalid .csv file "{file_path}"')
        return None
    
    if fileDF.shape[1] == 0:
        print(f'Provided file "{file_path}" is empty')
        return None
    
    if fileDF.shape[0] < n:
        print(f'Provided file "{file_path}" has less than {n} data points')
        return None
    
    random_starting_position = randrange(0, fileDF.shape[0] - n + 1)
    random_sample = fileDF.iloc[random_starting_position : random_starting_position + n]
        
    return random_sample

def get_outliers(data: pd.DataFrame):
    """
    Detects outlier Price values in the dataframe and returns those rows along
    with three more columns of stats:
    ['Mean of {row_count} values', 'Price - Mean', '% over threshold']

    Parameters
    ----------
    data : pandas.DataFrame
        A pandas DataFrame containing an arbitrary number of rows
        with columns ['Ticker', 'Timestamp', 'Price']

    Returns
    -------
    None if unsuccessful
    
    or
    
    a pandas DataFrame containing the same columns as the input dataframe,
    plus three more columns ['Mean of {row_count} values', 'Price - Mean',
    '% over threshold'], but only the rows considered outliers. 
    An outlier row has a Price column with a value over 2 standard deviations
    above the mean of the input
    
    """
    if data.shape[0] == 0:
        print('Input DataFrame contains no rows')
        return None
    
    column_names = ['Ticker', 'Timestamp', 'Price']
    if data.shape[1] != 3 or (data.columns.to_list() != column_names):
        print('Input DataFrame must have exactly three columns called',
               f'{column_names}')
        return None
    
    n = len(data['Price'])
    price_mean = sum(data['Price'].to_list()) / n
    std_deviation = math.sqrt(sum( [pow(x - price_mean, 2) for x in data['Price'].to_list()] ) / n)
    outliers = data[abs(data['Price'] - price_mean) > 2*std_deviation]
    mean_column_data = [ round(price_mean, 2) ] * len(outliers['Price'])
    outliers.insert(3, f'Mean of {n} sample', mean_column_data, True)
    price_mean_diff_data = [ round(diff, 2) for diff in outliers['Price'] - outliers[f'Mean of {n} sample'].to_list() ]
    outliers.insert(4, 'Price - Mean', price_mean_diff_data , True)
    percentage_over_threshold_data = [ round(100*(abs(diff_mean) / (2 * std_deviation)-1), 2) for diff_mean 
                    in outliers['Price - Mean'] ]
    outliers.insert(5, '% over threshold', percentage_over_threshold_data , True)
    return outliers

def main():
    local_folder_for_execution = 'stock_price_data_files'
    print("This program will go through each folder (representing a stock exchange) that is present in the",
          f"local folder called {local_folder_for_execution} and will look for outliers in a maximum number of files",
          "per stock exchange, depending on your input\n")
    root_path = os.getcwd()
    target_path = os.path.join(root_path, local_folder_for_execution)
    if not (os.path.exists(target_path) and os.path.isdir(target_path)):
        print(f'There is no folder called {local_folder_for_execution} for the program to run in')
        return None
    
    folder_content = os.listdir(target_path)
    if len(folder_content) == 0:
        print(f'Folder {local_folder_for_execution} is empty')
        return None
    
    n_files = input("Please enter the maximum number of files you wish to process per stock exchange:\n")
    if not n_files.isdigit():
        print('No files processed. Please use a positive non-zero integer value')
        return None
    
    n_files = int(n_files)
    
    date_time = datetime.now()
    output_folder_name = f"outliers_results_{date_time.date()}_{date_time.time().replace(microsecond=0).strftime('%H-%M-%S')}"
    
    n_sample_size = 30
    for folder_name in folder_content:
        curr_path = os.path.join(target_path, folder_name)
        if os.path.isdir(curr_path):
            file_cnt = 0
            for csv_filename in os.listdir(curr_path):
                if file_cnt >= n_files:
                    break
                    
                if csv_filename.endswith('.csv'):
                    csv_file_path = os.path.join(curr_path, csv_filename)
                    random_sample = get_n_random_consecutive_datapoints(csv_file_path, n_sample_size)
                    if random_sample is None:
                        continue
                    outliers = get_outliers(random_sample)
                    if outliers is None:
                        continue
                    if outliers.shape[0] == 0:
                        print(f'Sample from file {csv_file_path} returned no outliers. Output file was still created\n')
                    file_cnt += 1
                    output_folder_path = os.path.join(root_path, output_folder_name, folder_name)
                    if not os.path.exists(output_folder_path):
                        os.makedirs(output_folder_path)
                    output_file_path = os.path.join(output_folder_path, csv_filename)
                    outliers.to_csv(output_file_path, header=False, index=False)
            if file_cnt == 0:
                print(f'Folder {curr_path} contains no valid .csv files')

    print("Processing is finished")

if __name__ == '__main__':
    main()