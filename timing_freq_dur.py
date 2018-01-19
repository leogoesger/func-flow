import numpy as np
import os
import pandas as pd
import sys
from datetime import date, datetime

sys.path.append('utils/')

from helpers import is_multiple_date_data, 
from matrix_convert import convert_raw_data_to_matrix, sort_matrix
from calc_timing_freq_dur import calculate_timing_duration_frequency

np.warnings.filterwarnings('ignore')

start_date= '10/1'
directoryName = 'rawFiles'
endWith = '3.csv'

gauge_class_array = []
gauge_number_array = []

two_percent_exceedance_timing_array_ninety = []
two_percent_exceedance_timing_array_fifty = []
two_percent_exceedance_timing_array_ten = []
five_percent_exceedance_timing_array_ninety = []
five_percent_exceedance_timing_array_fifty = []
five_percent_exceedance_timing_array_ten = []
ten_percent_exceedance_timing_array_ninety = []
ten_percent_exceedance_timing_array_fifty = []
ten_percent_exceedance_timing_array_ten = []
twenty_percent_exceedance_timing_array_ninety = []
twenty_percent_exceedance_timing_array_fifty = []
twenty_percent_exceedance_timing_array_ten = []
fifty_percent_exceedance_timing_array_ninety = []
fifty_percent_exceedance_timing_array_fifty = []
fifty_percent_exceedance_timing_array_ten = []

two_percent_exceedance_freq_array_ninety = []
two_percent_exceedance_freq_array_fifty = []
two_percent_exceedance_freq_array_ten = []
five_percent_exceedance_freq_array_ninety = []
five_percent_exceedance_freq_array_fifty = []
five_percent_exceedance_freq_array_ten = []
ten_percent_exceedance_freq_array_ninety = []
ten_percent_exceedance_freq_array_fifty = []
ten_percent_exceedance_freq_array_ten = []
twenty_percent_exceedance_freq_array_ninety = []
twenty_percent_exceedance_freq_array_fifty = []
twenty_percent_exceedance_freq_array_ten = []
fifty_percent_exceedance_freq_array_ninety = []
fifty_percent_exceedance_freq_array_fifty = []
fifty_percent_exceedance_freq_array_ten = []

two_percent_exceedance_dur_array_ninety = []
two_percent_exceedance_dur_array_fifty = []
two_percent_exceedance_dur_array_ten = []
five_percent_exceedance_dur_array_ninety = []
five_percent_exceedance_dur_array_fifty = []
five_percent_exceedance_dur_array_ten = []
ten_percent_exceedance_dur_array_ninety = []
ten_percent_exceedance_dur_array_fifty = []
ten_percent_exceedance_dur_array_ten = []
twenty_percent_exceedance_dur_array_ninety = []
twenty_percent_exceedance_dur_array_fifty = []
twenty_percent_exceedance_dur_array_ten = []
fifty_percent_exceedance_dur_array_ninety = []
fifty_percent_exceedance_dur_array_fifty = []
fifty_percent_exceedance_dur_array_ten = []

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


               two_timing_median, two_dur_median, two_freq, five_timing_median, five_dur_median, five_freq, ten_timing_median, ten_dur_median, ten_freq, twenty_timing_median, twenty_dur_median, twenty_freq, fifty_timing_median, fifty_dur_median, fifty_freq = calculate_timing_duration_frequency(flow_matrix, year_ranges, start_date)

               two_percent_exceedance_timing_array_ninety.append(np.nanpercentile(two_timing_median, 90))
               two_percent_exceedance_timing_array_fifty.append(np.nanpercentile(two_timing_median, 50))
               two_percent_exceedance_timing_array_ten.append(np.nanpercentile(two_timing_median, 10))
               five_percent_exceedance_timing_array_ninety.append(np.nanpercentile(five_timing_median, 90))
               five_percent_exceedance_timing_array_fifty.append(np.nanpercentile(five_timing_median, 50))
               five_percent_exceedance_timing_array_ten.append(np.nanpercentile(five_timing_median, 10))
               ten_percent_exceedance_timing_array_ninety.append(np.nanpercentile(ten_timing_median, 90))
               ten_percent_exceedance_timing_array_fifty.append(np.nanpercentile(ten_timing_median, 50))
               ten_percent_exceedance_timing_array_ten.append(np.nanpercentile(ten_timing_median, 10))
               twenty_percent_exceedance_timing_array_ninety.append(np.nanpercentile(twenty_timing_median, 90))
               twenty_percent_exceedance_timing_array_fifty.append(np.nanpercentile(twenty_timing_median, 50))
               twenty_percent_exceedance_timing_array_ten.append(np.nanpercentile(twenty_timing_median, 10))
               fifty_percent_exceedance_timing_array_ninety.append(np.nanpercentile(fifty_timing_median, 90))
               fifty_percent_exceedance_timing_array_fifty.append(np.nanpercentile(fifty_timing_median, 50))
               fifty_percent_exceedance_timing_array_ten.append(np.nanpercentile(fifty_timing_median, 10))

               two_percent_exceedance_dur_array_ninety.append(np.nanpercentile(two_dur_median, 90))
               two_percent_exceedance_dur_array_fifty.append(np.nanpercentile(two_dur_median, 50))
               two_percent_exceedance_dur_array_ten.append(np.nanpercentile(two_dur_median, 10))
               five_percent_exceedance_dur_array_ninety.append(np.nanpercentile(five_dur_median, 90))
               five_percent_exceedance_dur_array_fifty.append(np.nanpercentile(five_dur_median, 50))
               five_percent_exceedance_dur_array_ten.append(np.nanpercentile(five_dur_median, 10))
               ten_percent_exceedance_dur_array_ninety.append(np.nanpercentile(ten_dur_median, 90))
               ten_percent_exceedance_dur_array_fifty.append(np.nanpercentile(ten_dur_median, 50))
               ten_percent_exceedance_dur_array_ten.append(np.nanpercentile(ten_dur_median, 10))
               twenty_percent_exceedance_dur_array_ninety.append(np.nanpercentile(twenty_dur_median, 90))
               twenty_percent_exceedance_dur_array_fifty.append(np.nanpercentile(twenty_dur_median, 50))
               twenty_percent_exceedance_dur_array_ten.append(np.nanpercentile(twenty_dur_median, 10))
               fifty_percent_exceedance_dur_array_ninety.append(np.nanpercentile(fifty_dur_median, 90))
               fifty_percent_exceedance_dur_array_fifty.append(np.nanpercentile(fifty_dur_median, 50))
               fifty_percent_exceedance_dur_array_ten.append(np.nanpercentile(fifty_dur_median, 10))

               two_percent_exceedance_freq_array_ninety.append(np.nanpercentile(two_freq, 90))
               two_percent_exceedance_freq_array_fifty.append(np.nanpercentile(two_freq, 50))
               two_percent_exceedance_freq_array_ten.append(np.nanpercentile(two_freq, 10))
               five_percent_exceedance_freq_array_ninety.append(np.nanpercentile(five_freq, 90))
               five_percent_exceedance_freq_array_fifty.append(np.nanpercentile(five_freq, 50))
               five_percent_exceedance_freq_array_ten.append(np.nanpercentile(five_freq, 10))
               ten_percent_exceedance_freq_array_ninety.append(np.nanpercentile(ten_freq, 90))
               ten_percent_exceedance_freq_array_fifty.append(np.nanpercentile(ten_freq, 50))
               ten_percent_exceedance_freq_array_ten.append(np.nanpercentile(ten_freq, 10))
               twenty_percent_exceedance_freq_array_ninety.append(np.nanpercentile(twenty_freq, 90))
               twenty_percent_exceedance_freq_array_fifty.append(np.nanpercentile(twenty_freq, 50))
               twenty_percent_exceedance_freq_array_ten.append(np.nanpercentile(twenty_freq, 10))
               fifty_percent_exceedance_freq_array_ninety.append(np.nanpercentile(fifty_freq, 90))
               fifty_percent_exceedance_freq_array_fifty.append(np.nanpercentile(fifty_freq, 50))
               fifty_percent_exceedance_freq_array_ten.append(np.nanpercentile(fifty_freq, 10))

               flow_matrix = np.vstack((year_ranges, flow_matrix))

               np.savetxt("processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
               current_gaguge_column_index = current_gaguge_column_index + step


result_matrix = np.vstack((gauge_class_array, gauge_number_array))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_timing_array_ninety))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_timing_array_fifty))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_timing_array_ten))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_timing_array_ninety))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_timing_array_fifty))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_timing_array_ten))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_timing_array_ninety))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_timing_array_fifty))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_timing_array_ten))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_timing_array_ninety))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_timing_array_fifty))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_timing_array_ten))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_timing_array_ninety))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_timing_array_fifty))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_timing_array_ten))

result_matrix = np.vstack((result_matrix, two_percent_exceedance_dur_array_ninety))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_dur_array_fifty))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_dur_array_ten))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_dur_array_ninety))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_dur_array_fifty))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_dur_array_ten))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_dur_array_ninety))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_dur_array_fifty))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_dur_array_ten))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_dur_array_ninety))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_dur_array_fifty))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_dur_array_ten))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_dur_array_ninety))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_dur_array_fifty))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_dur_array_ten))

result_matrix = np.vstack((result_matrix, two_percent_exceedance_freq_array_ninety))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_freq_array_fifty))
result_matrix = np.vstack((result_matrix, two_percent_exceedance_freq_array_ten))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_freq_array_ninety))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_freq_array_fifty))
result_matrix = np.vstack((result_matrix, five_percent_exceedance_freq_array_ten))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_freq_array_ninety))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_freq_array_fifty))
result_matrix = np.vstack((result_matrix, ten_percent_exceedance_freq_array_ten))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_freq_array_ninety))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_freq_array_fifty))
result_matrix = np.vstack((result_matrix, twenty_percent_exceedance_freq_array_ten))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_freq_array_ninety))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_freq_array_fifty))
result_matrix = np.vstack((result_matrix, fifty_percent_exceedance_freq_array_ten))

result_matrix = sort_matrix(result_matrix,0)

np.savetxt("processedFiles/result_matrix.csv", result_matrix, delimiter=",")
