import numpy as np
import math
import pandas as pd
from datetime import date, datetime
from helpers import calculate_std_each_column, is_multiple_date_data, extract_current_data_at_index, remove_nan_from_date_and_flow_columns, extract_info_from_date, convert_raw_data_to_matrix, calculate_average_each_column, calculate_cov_each_column

def _convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index):
    """Local function to convert raw data to matrix
    """
    current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column = extract_current_data_at_index(fixed_df, current_gaguge_column_index)
    date_column, flow_column = remove_nan_from_date_and_flow_columns(raw_date_column, raw_flow_column)
    years, julian_date, number_of_years = extract_info_from_date(date_column)

    flow_matrix = convert_raw_data_to_matrix(years, julian_date, flow_column, number_of_years)
    return current_gauge_class, current_gauge_number, flow_matrix


fixed_df = pd.read_csv('rawFiles/Data_3.csv', sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')


if is_multiple_date_data(fixed_df):
    print('Current Datset uses one date per column of data')
    step = 2
else:
    print('Current Datset uses the same date per column of data')
    step = 1

current_gaguge_column_index = 1

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

while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

    current_gauge_class, current_gauge_number, flow_matrix = _convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index)
    print('Gaguge Class: {}'.format(current_gauge_class))
    print('Gauge Number: {}'.format(current_gauge_number))

    """General Info"""
    gauge_class_array.append(current_gauge_class)
    gauge_number_array.append(current_gauge_number)

    average_each_column = calculate_average_each_column(flow_matrix)
    std_each_column = calculate_std_each_column(flow_matrix)
    cov_column = calculate_cov_each_column(std_each_column, average_each_column)

    flow_matrix = np.vstack((flow_matrix, np.full(len(cov_column), -999)))
    flow_matrix = np.vstack((flow_matrix, np.array(average_each_column)))
    flow_matrix = np.vstack((flow_matrix, np.array(std_each_column)))
    flow_matrix = np.vstack((flow_matrix, np.array(cov_column)))

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
result_matrix = np.vstack((result_matrix, average_average_array))
result_matrix = np.vstack((result_matrix, ten_percentile_array))
result_matrix = np.vstack((result_matrix, fifty_percentile_array))
result_matrix = np.vstack((result_matrix, ninty_percentile_array))
result_matrix = np.vstack((result_matrix, ten_percentile_cov_array))
result_matrix = np.vstack((result_matrix, fifty_percentile_cov_array))
result_matrix = np.vstack((result_matrix, ninty_percentile_cov_array))

np.savetxt("processedFiles/result_matrix_3.csv", result_matrix, delimiter=",")
