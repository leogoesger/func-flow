import numpy as np
import math
import pandas as pd
from datetime import date, datetime
from helpers import is_multiple_date_data, extract_current_data_at_index, remove_nan_from_date_and_flow_columns, extract_info_from_date, convert_raw_data_to_matrix, calculate_average_each_column

def _convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index):
    """Local function to convert raw data to matrix
    """
    current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column = extract_current_data_at_index(fixed_df, current_gaguge_column_index)
    date_column, flow_column = remove_nan_from_date_and_flow_columns(raw_date_column, raw_flow_column)
    years, julian_date, number_of_years = extract_info_from_date(date_column)

    flow_matrix = convert_raw_data_to_matrix(years, julian_date, flow_column, number_of_years)
    return current_gauge_class, current_gauge_number, flow_matrix


fixed_df = pd.read_csv('DATA/DATA3.csv', sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')


if is_multiple_date_data(fixed_df):
    print('Current Datset uses one date per column of data')
    step = 2
else:
    print('Current Datset uses the same date per column of data')
    step = 1

current_gaguge_column_index = 1
gauge_class_array = []
gauge_number_array = []
ten_percentile_array = []
fifty_percentile_array = []
ninty_percentile_array = []
while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):
    print('current_gaguge_column_index: {}...'.format(current_gaguge_column_index))

    current_gauge_class, current_gauge_number, flow_matrix = _convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index)

    gauge_class_array.append(current_gauge_class)
    gauge_number_array.append(current_gauge_number)
    ten_percentile_array.append(np.nanpercentile(calculate_average_each_column(flow_matrix), 10))
    fifty_percentile_array.append(np.nanpercentile(calculate_average_each_column(flow_matrix), 50))
    ninty_percentile_array.append(np.nanpercentile(calculate_average_each_column(flow_matrix), 90))

    #np.savetxt("processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
    current_gaguge_column_index = current_gaguge_column_index + step

result_matrix = np.vstack((gauge_class_array, gauge_number_array))
result_matrix = np.vstack((result_matrix, ten_percentile_array))
result_matrix = np.vstack((result_matrix, fifty_percentile_array))
result_matrix = np.vstack((result_matrix, ninty_percentile_array))

np.savetxt("processedFiles/result_matrix_3.csv", result_matrix, delimiter=",")

# print('Class: {}'.format(gauge_class_array))
# print('Number: {}'.format(gauge_number_array))
# print('10th Percentille: {}'.format(ten_percentile_array))
# print('50th Percentille: {}'.format(fifty_percentile_array))
# print('90th Percentille: {}'.format(ninty_percentile_array))
