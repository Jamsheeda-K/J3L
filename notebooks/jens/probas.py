import pandas as pd
import tqdm
from src.load_data import load_supermarket_data

df = load_supermarket_data('data')

locations = list(df['location'].unique())
locations.append('out')

dfg = df.groupby([df.index.weekday,'customer_no'],as_index=False)

freq_table = pd.DataFrame(0, index=locations, columns=locations, dtype=int)
init_series = pd.Series(0, index=locations, dtype=int)

# slow: takes 5 min on my computer
for x in tqdm.tqdm(dfg):
    cstm = x[1]['location'].resample('1min').ffill()
    dfcross = pd.crosstab(cstm, cstm.shift(-1))
    freq_table.loc[dfcross.index,dfcross.columns] += dfcross
    freq_table.loc[cstm.iloc[-1],'out'] += 1
    init_series.loc[cstm.iloc[1]] += 1

freq_table.loc['out','out'] = 1
freq_table.to_csv('data/freq_table.csv')

