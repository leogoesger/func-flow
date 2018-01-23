import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix
from utils.calc_start_of_summer import start_of_summer

np.warnings.filterwarnings('ignore')


def start_of_summer(start_date, directoryName, endWith):

    gauge_class_array = []
    gauge_number_array = []

    ten_percentile_sos_array = []
    fifty_percentile_sos_array = []
    ninety_percentile_sos_array = []


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


                   current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)
                   print('Gaguge Class: {}'.format(current_gauge_class))
                   print('Gauge Number: {}'.format(current_gauge_number))

                   """General Info"""
                   gauge_class_array.append(current_gauge_class)
                   gauge_number_array.append(current_gauge_number)

                   """#26: start of summer"""
                   start_of_summer_date_ten, start_of_summer_date_fifty, start_of_summer_date_ninety = start_of_summer(flow_matrix,start_date)

                   ten_percentile_sos_array.append(start_of_summer_date_ten)
                   fifty_percentile_sos_array.append(start_of_summer_date_fifty)
                   ninety_percentile_sos_array.append(start_of_summer_date_ninety)

                   flow_matrix = np.vstack((year_ranges, flow_matrix))

                   np.savetxt("post-processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
                   current_gaguge_column_index = current_gaguge_column_index + step



    result_matrix = np.vstack((gauge_class_array, gauge_number_array))
    result_matrix = np.vstack((result_matrix, ten_percentile_sos_array))
    result_matrix = np.vstack((result_matrix, fifty_percentile_sos_array))
    result_matrix = np.vstack((result_matrix, ninety_percentile_sos_array))
    result_matrix = sort_matrix(result_matrix,0)

    np.savetxt("post-processedFiles/sos_result_matrix.csv", result_matrix, delimiter=",")
