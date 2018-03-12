"""
Convert USGS File(s) to Data files for processing.
"""
import os
import csv
import numpy as np
import pandas as pd

from gauge_reference import regular_gauges


directory_name = 'rawFiles/Data_2'
end_with = '.csv'
newDF = pd.DataFrame()

counter = 1
for root,dirs,files in os.walk(directory_name):
    for file in files:
       if file.endswith(end_with):
           print('{}: {}'.format(counter, file[:-4]))


           fixed_df = pd.read_csv('{}/{}'.format(directory_name, file), sep='\t', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
           if int(fixed_df.iloc[10,-1]) in regular_gauges:
               insert_data = pd.DataFrame({0:np.nan, 1:99, 2:99, 3:99, 4:99, 5:99, 6:99}, index=['class'])
               new_fixed_df = pd.concat([insert_data, fixed_df])

               date = new_fixed_df.iloc[:,0]
               flow = new_fixed_df.iloc[:,1]
               flow.iloc[0] = regular_gauges[int(file[:-4])]['class']
               flow.iloc[1] = fixed_df.iloc[10,-1]

               newDF = pd.concat([newDF, date], axis=1)
               newDF = pd.concat([newDF, flow], axis=1)
           else:
               print('Missing Gauge: {}'.format(file[:-4]))
           counter = counter + 1

newDF.to_csv('../rawFiles/new_postProcess_2.csv', sep=',', index=False, header=False)
