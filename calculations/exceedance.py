import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header

np.warnings.filterwarnings('ignore')


def exceedance(start_date, directoryName, endWith):
    exceedance_percent = [2, 5, 10, 20, 50]
    column_header = ['Class', 'Gauge #', '2%', '5%', '10%', '20%', '50%']

    gauge_class_array = []
    gauge_number_array = []

    percent_exceedance = {}

    for percent in exceedance_percent:
        percent_exceedance[percent] = []


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

                   for percent in exceedance_percent:
                       percent_exceedance[percent].append(np.nanpercentile(flow_matrix, 100 - percent))

                   flow_matrix = np.vstack((year_ranges, flow_matrix))

                   np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(current_gauge_class), int(current_gauge_number)), flow_matrix, delimiter=",")
                   current_gaguge_column_index = current_gaguge_column_index + step



    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in exceedance_percent:
        result_matrix.append(percent_exceedance[percent])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/exceedance_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
