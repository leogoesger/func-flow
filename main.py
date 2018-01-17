import numpy as np
import math
import os
import pandas as pd
from datetime import date, datetime
from helpers import calculate_std_each_column, is_multiple_date_data, convert_raw_data_to_matrix, calculate_average_each_column, calculate_cov_each_column, calculate_percent_exceedance, sort_matrix

np.warnings.filterwarnings('ignore')

start_date= '10/1'
directoryName = 'rawFiles'

gauge_class_array = []
gauge_number_array = []

average_average_array = []

ten_percentile_array = []
fifty_percentile_array = []
ninty_percentile_array = []

ten_percentile_cov_array = []
fifty_percentile_cov_array = []
ninty_percentile_cov_array = []
average_average_cov_array = []

two_percent_exceedance_array = []
five_percent_exceedance_array = []
ten_percent_exceedance_array = []
twenty_percent_exceedance_array = []
fifty_percent_exceedance_array = []


for root,dirs,files in os.walk(directoryName):
    for file in files:
       if file.endswith(".csv"):


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
               print('Gaguge Class: {}'.format(current_gauge_class))
               print('Gauge Number: {}'.format(current_gauge_number))

               """General Info"""
               gauge_class_array.append(current_gauge_class)
               gauge_number_array.append(current_gauge_number)

               average_each_column = calculate_average_each_column(flow_matrix)
               std_each_column = calculate_std_each_column(flow_matrix)
               cov_column = calculate_cov_each_column(std_each_column, average_each_column)

               flow_matrix = np.vstack((year_ranges, flow_matrix))
               flow_matrix = np.vstack((flow_matrix, np.full(len(cov_column), -999)))
               flow_matrix = np.vstack((flow_matrix, np.array(average_each_column)))
               flow_matrix = np.vstack((flow_matrix, np.array(std_each_column)))
               flow_matrix = np.vstack((flow_matrix, np.array(cov_column)))

               """#1: two percent exceedance"""
               two_percent_exceedance_array.append(calculate_percent_exceedance(flow_matrix, 98))

               """#2: five percent exceedance"""
               five_percent_exceedance_array.append(calculate_percent_exceedance(flow_matrix, 95))

               """#3: ten percent exceedance"""
               ten_percent_exceedance_array.append(calculate_percent_exceedance(flow_matrix, 90))

               """#4: twenty percent exceedance"""
               twenty_percent_exceedance_array.append(calculate_percent_exceedance(flow_matrix, 80))

               """#5: fifty percent exceedance"""
               fifty_percent_exceedance_array.append(calculate_percent_exceedance(flow_matrix, 50))

               """#35: average of average"""
               average_average_array.append(np.nanmean(average_each_column))

               """#35: 10th, 50th and 90th of average"""
               ten_percentile_array.append(np.nanpercentile(average_each_column, 10))
               fifty_percentile_array.append(np.nanpercentile(average_each_column, 50))
               ninty_percentile_array.append(np.nanpercentile(average_each_column, 90))

               """#34: 10th, 50th and 90th of cov"""
               ten_percentile_cov_array.append(np.nanpercentile(cov_column, 10))
               fifty_percentile_cov_array.append(np.nanpercentile(cov_column, 50))
               ninty_percentile_cov_array.append(np.nanpercentile(cov_column, 90))

               np.savetxt("processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
               current_gaguge_column_index = current_gaguge_column_index + step


result_matrix = np.vstack((gauge_class_array, gauge_number_array))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_array))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_array))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_array))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_array))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_array))
result_matrix = np.vstack((result_matrix, average_average_array))
result_matrix = np.vstack((result_matrix, ten_percentile_array))
result_matrix = np.vstack((result_matrix, fifty_percentile_array))
result_matrix = np.vstack((result_matrix, ninty_percentile_array))
result_matrix = np.vstack((result_matrix, ten_percentile_cov_array))
result_matrix = np.vstack((result_matrix, fifty_percentile_cov_array))
result_matrix = np.vstack((result_matrix, ninty_percentile_cov_array))

result_matrix = sort_matrix(result_matrix,0)

np.savetxt("processedFiles/result_matrix.csv", result_matrix, delimiter=",")
