import os
from datetime import datetime
import numpy as np
import pandas as pd
from utils.helpers import is_multiple_date_data, smart_plot, remove_offset_from_julian_date
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from classes.Gauge import Gauge

np.warnings.filterwarnings('ignore')


def fall_flush(start_date, directoryName, endWith, class_number, gauge_numbers, plot):
    percentilles = [10, 50, 90]
    julian_start_date = datetime.strptime("{}/2001".format(start_date), "%m/%d/%Y").timetuple().tm_yday

    gauge_class_array = []
    gauge_number_array = []
    fall_timings = {}
    fall_magnitudes = {}
    fall_durations = {}
    fall_wet_timings = {}
    for percent in percentilles:
        fall_timings[percent] = []
        fall_magnitudes[percent] = []
        fall_durations[percent] = []
        fall_wet_timings[percent] = []

    for root, dirs, files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):

                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',',
                                       encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df)

                current_gaguge_column_index = 1
                if not class_number and not gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                            fixed_df, current_gaguge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_gauge = Gauge(
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        current_gauge.fall_flush_timings_durations()

                        for percent in percentilles:
                            current_gauge_fall_timing = np.nanpercentile(current_gauge.fall_timings, percent)
                            current_gauge_fall_wet_timing = np.nanpercentile(current_gauge.fall_wet_timings, percent)
                            current_gauge_fall_timing = remove_offset_from_julian_date(current_gauge_fall_timing, julian_start_date)
                            current_gauge_fall_wet_timing = remove_offset_from_julian_date(current_gauge_fall_wet_timing, julian_start_date)

                            fall_timings[percent].append(current_gauge_fall_timing)
                            fall_magnitudes[percent].append(np.nanpercentile(current_gauge.fall_magnitudes, percent))
                            fall_durations[percent].append(np.nanpercentile(current_gauge.fall_durations, percent))
                            fall_wet_timings[percent].append(current_gauge_fall_wet_timing)

                        current_gaguge_column_index = current_gaguge_column_index + step
                elif gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[1, current_gaguge_column_index]) in gauge_numbers:
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                                fixed_df, current_gaguge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_gauge = Gauge(
                                current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            current_gauge.fall_flush_timings_durations()

                            for percent in percentilles:
                                current_gauge_fall_timing = np.nanpercentile(current_gauge.fall_timings, percent)
                                current_gauge_fall_wet_timing = np.nanpercentile(current_gauge.fall_wet_timings, percent)
                                current_gauge_fall_timing = remove_offset_from_julian_date(current_gauge_fall_timing, julian_start_date)
                                current_gauge_fall_wet_timing = remove_offset_from_julian_date(current_gauge_fall_wet_timing, julian_start_date)

                                fall_timings[percent].append(current_gauge_fall_timing)
                                fall_magnitudes[percent].append(np.nanpercentile(current_gauge.fall_magnitudes, percent))
                                fall_durations[percent].append(np.nanpercentile(current_gauge.fall_durations, percent))
                                fall_wet_timings[percent].append(current_gauge_fall_wet_timing)

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

                            current_gauge.fall_flush_timings_durations()

                            for percent in percentilles:
                                current_gauge_fall_timing = np.nanpercentile(current_gauge.fall_timings, percent)
                                current_gauge_fall_wet_timing = np.nanpercentile(current_gauge.fall_wet_timings, percent)
                                current_gauge_fall_timing = remove_offset_from_julian_date(current_gauge_fall_timing, julian_start_date)
                                current_gauge_fall_wet_timing = remove_offset_from_julian_date(current_gauge_fall_wet_timing, julian_start_date)

                                fall_timings[percent].append(current_gauge_fall_timing)
                                fall_magnitudes[percent].append(np.nanpercentile(current_gauge.fall_magnitudes, percent))
                                fall_durations[percent].append(np.nanpercentile(current_gauge.fall_durations, percent))
                                fall_wet_timings[percent].append(current_gauge_fall_wet_timing)

                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')

    column_header = ['Class', 'Gauge', 'FAFL_Tim_10%', 'FAFL_Mag_10%', 'FAFL_Dur_10%', 'FA_Tim_Wet_10%', 'FAFL_Tim_50%', 'FAFL_Mag_50%', 'FAFL_Dur_50%', 'FA_Tim_Wet_50%', 'FAFL_Tim_90%', 'FAFL_Mag_90%', 'FAFL_Dur_90%', 'FA_Tim_Wet_90%']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in percentilles:
        result_matrix.append(fall_timings[percent])
        result_matrix.append(fall_magnitudes[percent])
        result_matrix.append(fall_durations[percent])
        result_matrix.append(fall_wet_timings[percent])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/fall_flush_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

    if plot:
        smart_plot(result_matrix)
