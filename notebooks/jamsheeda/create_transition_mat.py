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

#Transforming the dataframe for better implementation
transformed_df = df.reset_index().groupby(['customer_no','week_day'])[['timestamp','location']].agg(lambda x:list(x))

#creating transition matrix with before and after states
transition_df=pd.DataFrame(columns=['before','after'])
for i in transformed_df.iterrows():
    customer_no = i[0][0]
    week_day = i[0][1]
    time_stamp = i[1][0]
    sections = i[1][1]
    #print(sections)
    sections.insert(0,'entrance')
    time_stamp.insert(0,time_stamp[0])
    #print(sections)
    #print(time_stamp)
    for j in range(len(sections)):
        if (j+1)<len(sections):
            transition_df.loc[time_stamp[j]]=(sections[j],sections[j+1])

#resampling data to fill in every minute
resampled_df = transition_df.resample('1T').ffill()

#creating transition probability matrix
transition_probability_matrix = pd.crosstab(transition_df['before'], transition_df['after'], normalize=0)
transition_probability_matrix['entrance']=[0,0,0,0,0]
transition_probability_matrix.loc['checkout'] = [1,0,0,0,0,0]

# ordering the columns inside
transition_probability_matrix = pd.DataFrame(transition_probability_matrix,columns=['entrance','dairy','drinks','fruit','spices','checkout'],index=['entrance','dairy','drinks','fruit','spices','checkout'])
#print(transition_probability_matrix)


