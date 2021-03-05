#project: J3L
#author: jens
#date: 01.03.2021
#reading data from supermarket

import pandas as pd
#import os

files = [ 'monday.csv', 'tuesday.csv', 'friday.csv',      'thursday.csv',  'wednesday.csv' ]

def load_supermarket_data(data_dir):
    "read shop data from folder 'data_dir' into one pandas dataframe"
    dfs = []
    for x in files:
        #if(x=='freq_table.csv' | x=='supermarket.csv'): 
        #    continue
        df = pd.read_csv(data_dir + '/' + x, sep=';', parse_dates=True, infer_datetime_format=True)
        dfs.append(df)
    df = pd.concat(dfs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.set_index('timestamp')