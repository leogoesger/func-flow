import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data, plot_matrix
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_general_metric import calculate_std_each_column, calculate_average_each_column, calculate_cov_each_column

np.warnings.filterwarnings('ignore')

def coefficient_of_variance(start_date, directoryName, endWith):

    column_header = ['Class', 'Gauge #', 'average_average', 'average_10%', 'average_50%', 'average_ninty', 'cov_10%', 'cov_50%', 'cov_90%']

    gauge_class_array = []
    gauge_number_array = []

    average_average_array = []

    ten_percentile_average_array = []
    fifty_percentile_average_array = []
    ninety_percentile_average_array = []

    ten_percentile_cov_array = []
    fifty_percentile_cov_array = []
    ninety_percentile_cov_array = []
    average_average_cov_array = []


    for root,dirs,files in os.walk(directoryName):
        for file in files:
           if file.endswith(endWith):

               fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
               step = is_multiple_date_data(fixed_df);

               current_gaguge_column_index = 1
               while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                   current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                   """General Info"""
                   gauge_class_array.append(current_gauge_class)
                   gauge_number_array.append(current_gauge_number)

                   average_each_column = calculate_average_each_column(flow_matrix)
                   std_each_column = calculate_std_each_column(flow_matrix)
                   cov_column = calculate_cov_each_column(std_each_column, average_each_column)


                   """#35: average of average"""
                   average_average_array.append(np.nanmean(average_each_column))

                   """#35: 10th, 50th and 90th of average"""
                   ten_percentile_average_array.append(np.nanpercentile(average_each_column, 10))
                   fifty_percentile_average_array.append(np.nanpercentile(average_each_column, 50))
                   ninety_percentile_average_array.append(np.nanpercentile(average_each_column, 90))

                   """#34: 10th, 50th and 90th of cov"""
                   ten_percentile_cov_array.append(np.nanpercentile(cov_column, 10))
                   fifty_percentile_cov_array.append(np.nanpercentile(cov_column, 50))
                   ninety_percentile_cov_array.append(np.nanpercentile(cov_column, 90))

                   flow_matrix = np.vstack((year_ranges, flow_matrix))
                   flow_matrix = np.vstack((flow_matrix, np.full(len(cov_column), -999)))
                   flow_matrix = np.vstack((flow_matrix, np.array(average_each_column)))
                   flow_matrix = np.vstack((flow_matrix, np.array(std_each_column)))
                   flow_matrix = np.vstack((flow_matrix, np.array(cov_column)))

                   np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
                   current_gaguge_column_index = current_gaguge_column_index + step


    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)
    result_matrix.append(average_average_array)
    result_matrix.append(ten_percentile_average_array)
    result_matrix.append(fifty_percentile_average_array)
    result_matrix.append(ninety_percentile_average_array)
    result_matrix.append(ten_percentile_cov_array)
    result_matrix.append(fifty_percentile_cov_array)
    result_matrix.append(ninety_percentile_cov_array)

    result_matrix = sort_matrix(result_matrix,0)
    plot_matrix(result_matrix)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/cov_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
