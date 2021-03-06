import pandas as pd 
import numpy as np
import os

# Loading the customer movement data for 5 days
directory_in_str = "./data/supermarket/"
directory = os.fsencode(directory_in_str)
data = []
for filename in os.listdir(directory):
    df_temp = pd.read_csv(directory_in_str+filename.decode('utf-8'),sep=';',index_col=0,parse_dates=True)
    df_temp['week_day'] = filename.decode('utf-8').split(".")[0]
    data.append(df_temp)
df = pd.concat(data)

# to capture the time factor also we need to regularise to 1 min interval
new_df= df.groupby(['customer_no','week_day'])['location'].resample('1T').ffill()

# transforming matrix
transformed_df = new_df.reset_index().groupby(['customer_no','week_day'])[['timestamp','location']].agg(lambda x:list(x))

#creating transition matrix with before and after states
transition_df=pd.DataFrame(columns=['before','after'])
index = 0
for i in transformed_df.iterrows():
    customer_no = i[0][0]
    week_day = i[0][1]
    time_stamp = i[1][0]
    sections = i[1][1]
    sections.insert(0,'entrance')
    entrance_time = pd.to_datetime(time_stamp[0]) + pd.to_timedelta(-1, unit='m')
    time_stamp.insert(0,entrance_time)
    for j in range(len(sections)):
        if (j+1)<len(sections):
            transition_df.loc[index]=(sections[j],sections[j+1])
            index += 1

#creating transition probability matrix
transition_probability_matrix = pd.crosstab(transition_df['before'], transition_df['after'], normalize=0)
transition_probability_matrix['entrance']=[0,0,0,0,0]
transition_probability_matrix.loc['checkout'] = [1,0,0,0,0,0]

# ordering the columns inside
transition_probability_matrix = pd.DataFrame(transition_probability_matrix,columns=['entrance','dairy','drinks','fruit','spices','checkout'],index=['entrance','dairy','drinks','fruit','spices','checkout'])
assert all(transition_probability_matrix.sum(axis=1) > 0.999)
print(transition_probability_matrix)

# save to csv file
transition_probability_matrix.to_csv('transition_matrix.csv')
