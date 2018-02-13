import os
import numpy as np
import pandas as pd
from utils.helpers import is_multiple_date_data, smart_plot
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_annual_flow_metrics import Gauge

np.warnings.filterwarnings('ignore')


def all_year(start_date, directoryName, endWith, class_number, gauge_number):
    percentilles = [10, 50, 90]

    gauge_class_array = []
    gauge_number_array = []
    average_annual_flows = {}
    standard_deviations = {}
    coefficient_variations = {}
    for percent in percentilles:
        average_annual_flows[percent] = []
        standard_deviations[percent] = []
        coefficient_variations[percent] = []

    for root, dirs, files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):

                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',',
                                       encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df)

                current_gaguge_column_index = 1
                if not class_number and not gauge_number:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                            fixed_df, current_gaguge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.all_year()

                        for percent in percentilles:
                            average_annual_flows[percent].append(np.nanpercentile(current_gauge.average_annual_flows, percent))
                            standard_deviations[percent].append(np.nanpercentile(current_gauge.standard_deviations, percent))
                            coefficient_variations[percent].append(np.nanpercentile(current_gauge.coefficient_variations, percent))

                        current_gaguge_column_index = current_gaguge_column_index + step
                elif gauge_number:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[1, current_gaguge_column_index]) == int(gauge_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                                fixed_df, current_gaguge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_gauge = Gauge(
                                current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            current_gauge.all_year()

                            for percent in percentilles:
                                average_annual_flows[percent].append(np.nanpercentile(current_gauge.average_annual_flows, percent))
                                standard_deviations[percent].append(np.nanpercentile(current_gauge.standard_deviations, percent))
                                coefficient_variations[percent].append(np.nanpercentile(current_gauge.coefficient_variations, percent))

                        current_gaguge_column_index = current_gaguge_column_index + step

                elif class_number:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                                fixed_df, current_gaguge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_gauge = Gauge(
                                current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            current_gauge.all_year()

                            for percent in percentilles:
                                average_annual_flows[percent].append(np.nanpercentile(current_gauge.average_annual_flows, percent))
                                standard_deviations[percent].append(np.nanpercentile(current_gauge.standard_deviations, percent))
                                coefficient_variations[percent].append(np.nanpercentile(current_gauge.coefficient_variations, percent))

                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')

    column_header = ['Class', 'Gauge #', 'avg_10%', 'std_10%', 'cv_10%', 'avg_50%', 'std_50%', 'cv_50%', 'avg_90%', 'std_90%', 'cv_90%']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in percentilles:
        result_matrix.append(average_annual_flows[percent])
        result_matrix.append(standard_deviations[percent])
        result_matrix.append(coefficient_variations[percent])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/all_year_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
    smart_plot(result_matrix)
