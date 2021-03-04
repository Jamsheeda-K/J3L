'''
Data exploration of Doodl supermarket customer movements 
in supermarket. First data analysis
'''
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt

# read all data files in data frame
# pre-process timestamp as datetime and add one column for weekday
# create pandas data frame from all single files
path = r'/Users/Lutz/Desktop/spiced_projects/discrete-dill-student-code/J3L/data' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, delimiter=';', index_col=None, header=0)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    #df['day'] = df.iloc[0,0].dayofweek
    df['day'] = df['timestamp'].dt.day_name()
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame = frame.set_index('timestamp')
frame = frame.sort_values('timestamp', ascending=True)

# save create dataframe
frame.to_csv('/Users/Lutz/Desktop/spiced_projects/discrete-dill-student-code/J3L/notebooks/lutz/supermarket.csv')

print(frame.shape)
print(frame.head())
print(f'all data : {frame}')

# print heatmap to detect zero data
sns.heatmap(frame.isnull(), cbar = False)
plt.show()

# Calculate the total number of customers in each section
frame_cust_section = frame.groupby('location').count()['customer_no']
print(frame_cust_section)

# Calculate the total number of customers in each section over time 
frame_time_section = frame.reset_index().groupby(['timestamp', 'location'], as_index=False)['customer_no'].count()
print(frame_time_section)

# plot over all sections and time
g = sns.FacetGrid(frame_time_section, row="location",aspect=4,sharex=False)
g.map(sns.lineplot,'timestamp','customer_no')
plt.show()

#Display the number of customers at checkout over time
frame_checkout = frame[frame['location'] == 'checkout']
frame_checkout['customer_no'].resample('1H').count().plot(figsize=(15,6))
plt.show()

# Calculate the time each customer spent in the market
frame_min = frame.groupby(['day','customer_no'],as_index=False)['timestamp'].min()
frame_max = frame.groupby(['day','customer_no'],as_index=False)['timestamp'].max()
frame_time_market = frame_max['timestamp']-frame_min['timestamp']
print(f'frame_time_market

# Calculate the total number of customers in the supermarket over time.
frame_all_cust = frame.drop_duplicates(['customer_no'])
frame_all_cust['customer_no'].count()

""" 
Calculate the total number of customers in each section over time
Display the number of customers at checkout over time
Calculate the time each customer spent in the market
Calculate the total number of customers in the supermarket over time.
Our business managers think that the first section customers visit follows a different pattern than the     following ones. Plot the distribution of customers of their first visited section versus following sections (treat all sections visited after the first as “following”). """