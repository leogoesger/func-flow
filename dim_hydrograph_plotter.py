import numpy as np
import os
import pandas as pd
import sys
from datetime import date, datetime
import matplotlib.pyplot as plt

sys.path.append('utils/')

from helpers import is_multiple_date_data
from matrix_convert import convert_raw_data_to_matrix, sort_matrix
from calc_start_of_summer import start_of_summer
from general_metric_calc import calculate_average_each_row

np.warnings.filterwarnings('ignore')

start_date= '10/1'
directoryName = 'testFiles'
endWith = '4.csv'

gauge_class_array = []
gauge_number_array = []
row_average = []


for root,dirs,files in os.walk(directoryName):
    for file in files:
        if file.endswith(endWith):
            
            fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
            
            if is_multiple_date_data(fixed_df):
                print('Current Datset uses one date per column of data')
                step = 2
            else:
                print('Current Datset uses the same date per column of data')
                step = 1
                
            current_gaguge_column_index = 1
            
            while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):
                
                current_gauge_class, current_gauge_number, year_ranges, flow_matrix = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)
                
                """General Info"""
                gauge_class_array.append(current_gauge_class)
                gauge_number_array.append(current_gauge_number)
                
                """Dimensionless Hydrograph Plotter"""
                row_average.append(calculate_average_each_row(flow_matrix))
                number_of_rows = len(flow_matrix)
                number_of_columns = len(flow_matrix[0,:])
                normalized_matrix = np.zeros((number_of_rows, number_of_columns))
                percentiles = np.zeros((number_of_rows, 5))
                
                for row_index, row_data in enumerate(flow_matrix[:,0]):
                    for column_index, column_data in enumerate(flow_matrix[row_index, :]):
                        normalized_matrix[row_index,column_index] = flow_matrix[row_index,column_index]/row_average[-1][row_index]
                
                    percentiles[row_index,0] = np.nanpercentile(normalized_matrix[row_index,:], 10)
                    percentiles[row_index,1] = np.nanpercentile(normalized_matrix[row_index,:], 25)
                    percentiles[row_index,2] = np.nanpercentile(normalized_matrix[row_index,:], 50)
                    percentiles[row_index,3] = np.nanpercentile(normalized_matrix[row_index,:], 75)
                    percentiles[row_index,4] = np.nanpercentile(normalized_matrix[row_index,:], 90)
                    
                plt.gca().set_color_cycle(['navy', 'deepskyblue', 'red', 'deepskyblue','navy'])
                x = np.arange(0,366,1)
                
                plt.plot(percentiles[:,0])
                plt.plot(percentiles[:,1])
                plt.plot(percentiles[:,2])
                plt.plot(percentiles[:,3])
                plt.plot(percentiles[:,4])
                plt.fill_between(x, percentiles[:,0], percentiles[:,1], color = 'powderblue')
                
                np.savetxt("post-processedFiles/Class-{}/{}qqqqqqq.csv".format(int(current_gauge_class), int(current_gauge_number)), normalized_matrix, delimiter=",")
                np.savetxt("post-processedFiles/Class-{}/{}percentiles.csv".format(int(current_gauge_class), int(current_gauge_number)), percentiles, delimiter=",")
                
                current_gaguge_column_index = current_gaguge_column_index + step


		
                   

			  
			 
               
               
               
                    
        
	  