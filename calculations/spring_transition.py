import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data, smart_plot
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_annual_flow_metrics import Gauge

np.warnings.filterwarnings('ignore')


def spring_transition(start_date, directoryName, endWith, class_number, gauge_number):
    percentilles = [20, 50, 90]

    gauge_class_array = []
    gauge_number_array = []
    spring_timings = {}
    spring_durations = {}
    spring_magnitudes = {}
    spring_rocs = {}
    for percent in percentilles:
        spring_timings[percent] = []
        spring_durations[percent] = []
        spring_magnitudes[percent] = []
        spring_rocs[percent] = []


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

                        current_gauge.spring_transition_timing_magnitude()
                        current_gauge.start_of_summer()
                        current_gauge.spring_transition_duration()
                        current_gauge.spring_transition_roc()

                        for percent in percentilles:
                            spring_timings[percent].append(np.nanpercentile(current_gauge.spring_timings, percent))
                            spring_durations[percent].append(np.nanpercentile(current_gauge.spring_durations, percent))
                            spring_magnitudes[percent].append(np.nanpercentile(current_gauge.spring_magnitudes, percent))
                            spring_rocs[percent].append(np.nanpercentile(current_gauge.spring_rocs, percent))

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

                            current_gauge.spring_transition_timing_magnitude()
                            current_gauge.start_of_summer()
                            current_gauge.spring_transition_duration()
                            current_gauge.spring_transition_roc()


                            for percent in percentilles:
                                spring_timings[percent].append(np.nanpercentile(current_gauge.spring_timings, percent))
                                spring_durations[percent].append(np.nanpercentile(current_gauge.spring_durations, percent))
                                spring_magnitudes[percent].append(np.nanpercentile(current_gauge.spring_magnitudes, percent))
                                spring_rocs[percent].append(np.nanpercentile(current_gauge.spring_rocs, percent))

                            break

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

                            current_gauge.spring_transition_timing_magnitude()
                            current_gauge.start_of_summer()
                            current_gauge.spring_transition_duration()
                            current_gauge.spring_transition_roc()

                            for percent in percentilles:
                                spring_timings[percent].append(np.nanpercentile(current_gauge.spring_timings, percent))
                                spring_durations[percent].append(np.nanpercentile(current_gauge.spring_durations, percent))
                                spring_magnitudes[percent].append(np.nanpercentile(current_gauge.spring_magnitudes, percent))
                                spring_rocs[percent].append(np.nanpercentile(current_gauge.spring_rocs, percent))

                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')

    column_header = ['Class', 'Gauge #', 'timing_20%', 'duration_20%', 'magnitude_20%', 'rate of change 20%', 'timing_50%', 'duration_50%', 'magnitude_50%', 'rate of change 50%', 'timing_90%', 'duration_90%', 'magnitude_90%', 'rate of change 90%']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in percentilles:
        result_matrix.append(spring_timings[percent])
        result_matrix.append(spring_durations[percent])
        result_matrix.append(spring_magnitudes[percent])
        result_matrix.append(spring_rocs[percent])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/spring_transition_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
    smart_plot(result_matrix)
