import pandas as pd
import numpy as np
import  os
import matplotlib.pyplot as plt

data_dir = './data/'

dfs = []
for x in os.listdir(data_dir):
    df = pd.read_csv(data_dir + x, sep=';', parse_dates=True, infer_datetime_format=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['day'] = df.iloc[0,0].dayofweek
    dfs.append(df)


df = pd.concat(dfs)

#Calculate the total number of customers in each section
print('number of customers each section (may be counting doubles)')
print(df.groupby(['location']).count()['customer_no'])

#Calculate the total number of customers in each section over time
print('number of customers each section (not counting doubles)')
dfg=df.groupby(['day', 'location','customer_no'],as_index=False).count()
print(dfg.value_counts('location'))

# Display the number of customers at checkout over time
filt = df['location']=='checkout'
df.loc[filt].set_index('timestamp').resample('2H')['customer_no'].count().plot(kind='bar',title='# customers at checkout')
plt.show()

# Calculate the time each customer spent in the market
df_min = df.groupby(['day','customer_no'],as_index=False)['timestamp'].min()
df_max = df.groupby(['day','customer_no'],as_index=False)['timestamp'].max()
df_time_costumer_in_market = df_max['timestamp']-df_min['timestamp']

#Calculate the total number of customers in the supermarket over time.
df_count = pd.Series(index=df['timestamp'], dtype=int)

for i in df_min.iterrows():
    costumer_in = i[1]['timestamp']
    df_count[costumer_in:] = df_count[costumer_in:] + 1

for i in df_max.iterrows():
    costumer_out = i[1]['timestamp']
    df_count[costumer_out:] = df_count[costumer_out:] -1

df_count.plot(title='# of customers over time')
plt.show()



