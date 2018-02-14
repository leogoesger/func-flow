import os
import numpy as np
import pandas as pd
from utils.helpers import is_multiple_date_data, smart_plot
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_annual_flow_metrics import Gauge

np.warnings.filterwarnings('ignore')


def summer_baseflow(start_date, directoryName, endWith, class_number, gauge_number):
    percentilles = [10, 50, 90]

    gauge_class_array = []
    gauge_number_array = []
    summer_timings = {}
    summer_10_magnitudes = {}
    summer_50_magnitudes = {}
    summer_flush_durations = {}
    summer_wet_durations = {}
    summer_no_flow_counts = {}

    for percentile in percentilles:
        summer_timings[percentile] = []
        summer_10_magnitudes[percentile] = []
        summer_50_magnitudes[percentile] = []
        summer_flush_durations[percentile] = []
        summer_wet_durations[percentile] = []
        summer_no_flow_counts[percentile] = []

    for root,dirs,files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):

                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df);

                current_gaguge_column_index = 1
                while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                    if gauge_number:
                        if int(fixed_df.iloc[1, current_gaguge_column_index]) == int(gauge_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            current_gauge.start_of_summer()
                            current_gauge.fall_flush_timings_durations()
                            current_gauge.summer_baseflow_durations_magnitude()
                            for percentile in percentilles:
                                summer_timings[percentile].append(np.nanpercentile(current_gauge.summer_timings, percentile))
                                summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                                summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                                summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                                summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                                summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                            break
                    elif not class_number and not gauge_number:
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.start_of_summer()
                        current_gauge.fall_flush_timings_durations()
                        current_gauge.summer_baseflow_durations_magnitude()
                        for percentile in percentilles:
                            summer_timings[percentile].append(np.nanpercentile(current_gauge.summer_timings, percentile))
                            summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                            summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                            summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                            summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                            summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                    elif int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.start_of_summer()
                        current_gauge.fall_flush_timings_durations()
                        current_gauge.summer_baseflow_durations_magnitude()
                        for percentile in percentilles:
                            summer_timings[percentile].append(np.nanpercentile(current_gauge.summer_timings, percentile))
                            summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                            summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                            summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                            summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                            summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                    current_gaguge_column_index = current_gaguge_column_index + step

    column_header = ['Class', 'Gauge #', 'timing_10%','mag_10%_10%','mag_50%_10%','dur_flush_10%', 'dur_wet_10%', 'dur_no_flow_10%', 'timing_50%','mag_10%_50%','mag_50%_50%','dur_flush_50%', 'dur_wet_50%', 'dur_no_flow_50%','timing_90%','mag_10%_90%','mag_50%_90%','dur_flush_90%', 'dur_wet_90%', 'dur_no_flow_90%']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percentile in percentilles:
        result_matrix.append(summer_timings[percentile])
        result_matrix.append(summer_10_magnitudes[percentile])
        result_matrix.append(summer_50_magnitudes[percentile])
        result_matrix.append(summer_flush_durations[percentile])
        result_matrix.append(summer_wet_durations[percentile])
        result_matrix.append(summer_no_flow_counts[percentile])

    result_matrix = sort_matrix(result_matrix,0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/summer_baseflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
    smart_plot(result_matrix)
