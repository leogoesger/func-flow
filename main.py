import numpy as np
import os
import pandas as pd
import sys
from datetime import date, datetime

sys.path.append('utils/')

from helpers import is_multiple_date_data, plot_matrix
from matrix_convert import convert_raw_data_to_matrix, sort_matrix
from general_metric_calc import calculate_std_each_column, calculate_average_each_column, calculate_cov_each_column, calculate_percent_exceedance
from calc_start_of_summer import start_of_summer
from calc_timing_freq_dur import calculate_timing_duration_frequency

np.warnings.filterwarnings('ignore')

start_date= '10/1'
directoryName = 'rawFiles'
endWith = '.csv'

gauge_class_array = []
gauge_number_array = []

average_average_array = []

ten_percentile_average_array = []
fifty_percentile_average_array = []
ninty_percentile_average_array = []

ten_percentile_cov_array = []
fifty_percentile_cov_array = []
ninty_percentile_cov_array = []
average_average_cov_array = []

two_percent_exceedance_array_ninety = []
two_percent_exceedance_array_fifty = []
two_percent_exceedance_array_ten = []
five_percent_exceedance_array_ninety = []
five_percent_exceedance_array_fifty = []
five_percent_exceedance_array_ten = []
ten_percent_exceedance_array_ninety = []
ten_percent_exceedance_array_fifty = []
ten_percent_exceedance_array_ten = []
twenty_percent_exceedance_array_ninety = []
twenty_percent_exceedance_array_fifty = []
twenty_percent_exceedance_array_ten = []
fifty_percent_exceedance_array_ninety = []
fifty_percent_exceedance_array_fifty = []
fifty_percent_exceedance_array_ten = []


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
               print('Gaguge Class: {}'.format(current_gauge_class))
               print('Gauge Number: {}'.format(current_gauge_number))

               """General Info"""
               gauge_class_array.append(current_gauge_class)
               gauge_number_array.append(current_gauge_number)

               average_each_column = calculate_average_each_column(flow_matrix)
               std_each_column = calculate_std_each_column(flow_matrix)
               cov_column = calculate_cov_each_column(std_each_column, average_each_column)

               """#26: start of summer"""
               if (start_date == '1/1'):
                   start_of_summer_array = start_of_summer(flow_matrix,start_date)

               two, five, ten, twenty, fifty = calculate_percent_exceedance(flow_matrix)

               """#1: two percent exceedance"""
               two_percent_exceedance_array_ninety.append(np.nanpercentile(two, 90))
               two_percent_exceedance_array_fifty.append(np.nanpercentile(two, 50))
               two_percent_exceedance_array_ten.append(np.nanpercentile(two, 10))

               """#2: five percent exceedance"""
               five_percent_exceedance_array_ninety.append(np.nanpercentile(five, 90))
               five_percent_exceedance_array_fifty.append(np.nanpercentile(five, 50))
               five_percent_exceedance_array_ten.append(np.nanpercentile(five, 10))

               """#3: ten percent exceedance"""
               ten_percent_exceedance_array_ninety.append(np.nanpercentile(ten, 90))
               ten_percent_exceedance_array_fifty.append(np.nanpercentile(ten, 50))
               ten_percent_exceedance_array_ten.append(np.nanpercentile(ten, 10))

               """#4: twenty percent exceedance"""
               twenty_percent_exceedance_array_ninety.append(np.nanpercentile(twenty, 90))
               twenty_percent_exceedance_array_fifty.append(np.nanpercentile(twenty, 50))
               twenty_percent_exceedance_array_ten.append(np.nanpercentile(twenty, 10))

               """#5: fifty percent exceedance"""
               fifty_percent_exceedance_array_ninety.append(np.nanpercentile(fifty, 90))
               fifty_percent_exceedance_array_fifty.append(np.nanpercentile(fifty, 50))
               fifty_percent_exceedance_array_ten.append(np.nanpercentile(fifty, 10))

               """#35: average of average"""
               average_average_array.append(np.nanmean(average_each_column))

               """#35: 10th, 50th and 90th of average"""
               ten_percentile_average_array.append(np.nanpercentile(average_each_column, 10))
               fifty_percentile_average_array.append(np.nanpercentile(average_each_column, 50))
               ninty_percentile_average_array.append(np.nanpercentile(average_each_column, 90))

               """#34: 10th, 50th and 90th of cov"""
               ten_percentile_cov_array.append(np.nanpercentile(cov_column, 10))
               fifty_percentile_cov_array.append(np.nanpercentile(cov_column, 50))
               ninty_percentile_cov_array.append(np.nanpercentile(cov_column, 90))

               flow_matrix = np.vstack((year_ranges, flow_matrix))
               flow_matrix = np.vstack((flow_matrix, np.full(len(cov_column), -999)))
               flow_matrix = np.vstack((flow_matrix, np.array(average_each_column)))
               flow_matrix = np.vstack((flow_matrix, np.array(std_each_column)))
               flow_matrix = np.vstack((flow_matrix, np.array(cov_column)))

               np.savetxt("processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
               current_gaguge_column_index = current_gaguge_column_index + step

if (start_date != '1/1'):
    result_matrix = np.vstack((gauge_class_array, gauge_number_array))
    result_matrix = np.vstack((result_matrix, two_percent_exceedance_array_ninety))
    result_matrix = np.vstack((result_matrix, two_percent_exceedance_array_fifty))
    result_matrix = np.vstack((result_matrix, two_percent_exceedance_array_ten))
    result_matrix = np.vstack((result_matrix, five_percent_exceedance_array_ninety))
    result_matrix = np.vstack((result_matrix, five_percent_exceedance_array_fifty))
    result_matrix = np.vstack((result_matrix, five_percent_exceedance_array_ten))
    result_matrix = np.vstack((result_matrix, ten_percent_exceedance_array_ninety))
    result_matrix = np.vstack((result_matrix, ten_percent_exceedance_array_fifty))
    result_matrix = np.vstack((result_matrix, ten_percent_exceedance_array_ten))
    result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_array_ninety))
    result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_array_fifty))
    result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_array_ten))
    result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_array_ninety))
    result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_array_fifty))
    result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_array_ten))
    result_matrix = np.vstack((result_matrix, average_average_array))
    result_matrix = np.vstack((result_matrix, ten_percentile_average_array))
    result_matrix = np.vstack((result_matrix, fifty_percentile_average_array))
    result_matrix = np.vstack((result_matrix, ninty_percentile_average_array))
    result_matrix = np.vstack((result_matrix, ten_percentile_cov_array))
    result_matrix = np.vstack((result_matrix, fifty_percentile_cov_array))
    result_matrix = np.vstack((result_matrix, ninty_percentile_cov_array))

    result_matrix = sort_matrix(result_matrix,0)

    plot_matrix(result_matrix)

    np.savetxt("processedFiles/result_matrix.csv", result_matrix, delimiter=",")
