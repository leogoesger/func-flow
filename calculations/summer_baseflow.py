import os
from datetime import datetime
import numpy as np
import pandas as pd
from utils.helpers import is_multiple_date_data, smart_plot, remove_offset_from_julian_date
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from classes.Gauge import Gauge

np.warnings.filterwarnings('ignore')


def summer_baseflow(start_date, directory_name, end_with, class_number, gauge_numbers, plot):
    percentilles = [10, 50, 90]
    julian_start_date = datetime.strptime("{}/2001".format(start_date), "%m/%d/%Y").timetuple().tm_yday

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

    for root,dirs,files in os.walk(directory_name):
        for file in files:
            if file.endswith(end_with):

                fixed_df = pd.read_csv('{}/{}'.format(directory_name, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df);

                current_gauge_column_index = 1
                while current_gauge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                    if gauge_numbers:
                        if int(fixed_df.iloc[1, current_gauge_column_index]) in gauge_numbers:
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            current_gauge.start_of_summer()
                            current_gauge.fall_flush_timings_durations()
                            current_gauge.summer_baseflow_durations_magnitude()

                            for percentile in percentilles:
                                current_gauge_summer_timing = np.nanpercentile(current_gauge.summer_timings, percentile)
                                current_gauge_summer_timing = remove_offset_from_julian_date(current_gauge_summer_timing, julian_start_date)

                                summer_timings[percentile].append(current_gauge_summer_timing)
                                summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                                summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                                summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                                summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                                summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                    elif not class_number and not gauge_numbers:
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.start_of_summer()
                        current_gauge.fall_flush_timings_durations()
                        current_gauge.summer_baseflow_durations_magnitude()

                        for percentile in percentilles:
                            current_gauge_summer_timing = np.nanpercentile(current_gauge.summer_timings, percentile)
                            current_gauge_summer_timing = remove_offset_from_julian_date(current_gauge_summer_timing, julian_start_date)

                            summer_timings[percentile].append(current_gauge_summer_timing)
                            summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                            summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                            summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                            summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                            summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                    elif int(fixed_df.iloc[0, current_gauge_column_index]) == int(class_number):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.start_of_summer()
                        current_gauge.fall_flush_timings_durations()
                        current_gauge.summer_baseflow_durations_magnitude()

                        for percentile in percentilles:
                            current_gauge_summer_timing = np.nanpercentile(current_gauge.summer_timings, percentile)
                            current_gauge_summer_timing = remove_offset_from_julian_date(current_gauge_summer_timing, julian_start_date)

                            summer_timings[percentile].append(current_gauge_summer_timing)
                            summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
                            summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
                            summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
                            summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
                            summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

                    current_gauge_column_index = current_gauge_column_index + step

    column_header = ['Class', 'Gauge', 'SU_Tim_10','SU_BFL_Mag_10_10','SU_BFL_Mag_50_10','SU_BFL_Dur_Flush_10', 'SU_BFL_Dur_Wet_10', 'SU_BFL_NoFlow_10', 'SU_Tim_50','SU_BFL_Mag_10_50','SU_BFL_Mag_50_50','SU_BFL_Dur_Flush_50', 'SU_BFL_Dur_Wet_50', 'SU_BFL_NoFlow_50','SU_Tim_90','SU_BFL_Mag_10_90','SU_BFL_Mag_50_90','SU_BFL_Dur_Flush_90', 'SU_BFL_Dur_Wet_90', 'SU_BFL_NoFlow_90']
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
    if plot:
        smart_plot(result_matrix)
