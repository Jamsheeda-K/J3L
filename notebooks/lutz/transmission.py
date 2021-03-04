'''
Creating a transition matrix and a crosstab
'''

import pandas as pd
import numpy as np
import pygraphviz as pgv

df = pd.read_csv('/Users/Lutz/Desktop/spiced_projects/discrete-dill-student-code/J3L/notebooks/lutz/supermarket.csv')


locations = list(df['location'].unique())
locations.append('out')
locations.append('in')

dfg = df.groupby([df.index.weekday,'customer_no'],as_index=False)

freq_table = pd.DataFrame(0, index=locations, columns=locations, dtype=int)

# slow: takes 5 min on my computer
for x in tqdm.tqdm(dfg):
    cstm = x[1]['location'].resample('1min').ffill()
    dfcross = pd.crosstab(cstm, cstm.shift(-1))
    freq_table.loc[dfcross.index,dfcross.columns] += dfcross
    freq_table.loc[cstm.iloc[-1],'out'] += 1
    freq_table.loc['in',cstm.iloc[0]] += 1

freq_table.loc['out','out'] = 1
freq_table.to_csv('data/freq_table.csv')

