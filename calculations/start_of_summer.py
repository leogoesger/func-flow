import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_start_of_summer import calc_start_of_summer

np.warnings.filterwarnings('ignore')


def start_of_summer(start_date, directoryName, endWith):

    column_header = ['Class', 'Gauge #', 'SOS_10%', 'SOS_50%', 'SOS_90%']

    gauge_class_array = []
    gauge_number_array = []

    ten_percentile_sos_array = []
    fifty_percentile_sos_array = []
    ninety_percentile_sos_array = []


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

                   """#26: start of summer"""
                   start_dates = calc_start_of_summer(flow_matrix, start_date)

                   ten_percentile_sos_array.append(np.nanpercentile(start_dates, 10))
                   fifty_percentile_sos_array.append(np.nanpercentile(start_dates, 50))
                   ninety_percentile_sos_array.append(np.nanpercentile(start_dates, 90))

                   flow_matrix = np.vstack((year_ranges, flow_matrix))

                   np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
                   current_gaguge_column_index = current_gaguge_column_index + step


    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)
    result_matrix.append(ten_percentile_sos_array)
    result_matrix.append(fifty_percentile_sos_array)
    result_matrix.append(ninety_percentile_sos_array)

    result_matrix = sort_matrix(result_matrix,0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/sos_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
