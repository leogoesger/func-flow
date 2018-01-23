"""
Convert USGS File(s) to Data files for processing.
"""
import os
import csv
import numpy as np
import pandas as pd

from gauge_reference import combined_gauges, old_gauges, new_gauges


directoryName = 'rawFiles/Data_2'
endWith = '.csv'
newDF = pd.DataFrame()

counter = 1
for root,dirs,files in os.walk(directoryName):
    for file in files:
       if file.endswith(endWith):
           print('{}: {}'.format(counter, file))

           fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep='\t', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
           insert_data = pd.DataFrame({0:np.nan, 1:99, 2:99, 3:99, 4:99, 5:99, 6:99}, index=['class'])
           new_fixed_df = pd.concat([insert_data, fixed_df])

           date = new_fixed_df.iloc[:,0]
           flow = new_fixed_df.iloc[:,1]
           flow.iloc[0] = combined_gauges[int(file[:-4])]
           flow.iloc[1] = fixed_df.iloc[10,-1]

           newDF = pd.concat([newDF, date], axis=1)
           newDF = pd.concat([newDF, flow], axis=1)
           counter = counter + 1

newDF.to_csv('../rawFiles/postProcess_2.csv', sep=',', index=False, header=False)
