import pandas as pd
import numpy as np
import  os

data_dir = './data/'

dfs = []
for i,x in enumerate(os.listdir(data_dir)):
    df = pd.read_csv(data_dir + x, sep=';', parse_dates=True, infer_datetime_format=True)
    df['day'] = i
    dfs.append(df)

df = pd.concat(dfs)
df['timestamp'] = pd.to_datetime(df['timestamp'])


print('number of customers each section (may be counting doubles)')
print(df.groupby(['location']).count()['customer_no'])

print('number of customers each section (not counting doubles)')
dfg=df.groupby(['day', 'location','customer_no'],as_index=False).count()
dfg.value_counts('location')
