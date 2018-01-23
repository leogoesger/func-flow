import numpy as np
import os
import pandas as pd
import sys
from datetime import date, datetime

sys.path.append('utils/')

from helpers import is_multiple_date_data
from matrix_convert import convert_raw_data_to_matrix, sort_matrix
from calc_timing_freq_dur import calculate_timing_duration_frequency

np.warnings.filterwarnings('ignore')

start_date= '10/1'
directoryName = 'rawFiles'
endWith = '3.csv'
exceedance_percent = [2, 5, 10, 20, 50]
percentilles = [10, 50, 90]

gauge_class_array = []
gauge_number_array = []

timing = {}
duration = {}
freq = {}

for percent in exceedance_percent:
    timing[percent] = {}
    duration[percent] = {}
    freq[percent] = {}
    for percentille in percentilles:
        timing[percent][percentille] = []
        duration[percent][percentille] = []
        freq[percent][percentille] = []


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
               print('Number: {}'.format(current_gaguge_column_index))
               current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

               """General Info"""
               gauge_class_array.append(current_gauge_class)
               gauge_number_array.append(current_gauge_number)


               current_timing, current_duration, current_freq = calculate_timing_duration_frequency(flow_matrix, year_ranges, start_date, exceedance_percent)

               for percent in current_timing:
                   for percentille in percentilles:

                       timing[percent][percentille].append(np.nanpercentile(np.array(current_timing[percent], dtype=np.float), percentille))
                       duration[percent][percentille].append(np.nanpercentile(current_duration[percent], percentille))
                       freq[percent][percentille].append(np.nanpercentile(current_freq[percent], percentille))

               # flow_matrix = np.vstack((year_ranges, flow_matrix))
               #
               # np.savetxt("post-processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")

               current_gaguge_column_index = current_gaguge_column_index + step


result_matrix = np.vstack((gauge_class_array, gauge_number_array))

for percent in current_timing:
    for percentille in percentilles:
        result_matrix = np.vstack((result_matrix, timing[percent][percentille]))
        result_matrix = np.vstack((result_matrix, duration[percent][percentille]))
        result_matrix = np.vstack((result_matrix, freq[percent][percentille]))

result_matrix = sort_matrix(result_matrix,0)

np.savetxt("post-processedFiles/timing_freq_dur_result_matrix.csv", result_matrix, delimiter=",")
