import os
import numpy as np
import pandas as pd

from utils.helpers import is_multiple_date_data, smart_plot
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_winter_highflow import calc_winter_highflow_POR, GaugeInfo
from utils.calc_annual_flow_metrics import Gauge

np.warnings.filterwarnings('ignore')


def winter_highflow_annual(start_date, directoryName, endWith, class_number, gauge_numbers, plot):
    exceedance_percent = [2, 5, 10, 20, 50]
    percentilles = [10, 50, 90]

    gauge_class_array = []
    gauge_number_array = []

    timing = {}
    duration = {}
    freq = {}

    for percent in exceedance_percent:
        timing[percent] = {}
        duration[percent] = {}
        freq[percent] = {}
        for percentille in percentilles:
            timing[percent][percentille] = []
            duration[percent][percentille] = []
            freq[percent][percentille] = []

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

                        current_gauge.winter_highflow_annual()

                        for percent in exceedance_percent:
                            for percentille in percentilles:
                                timing[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_timings[percent], dtype=np.float), percentille))
                                duration[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_durations[percent], dtype=np.float), percentille))
                                freq[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_frequencys[percent], dtype=np.float), percentille))

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

                            current_gauge.winter_highflow_annual()

                            for percent in exceedance_percent:
                                for percentille in percentilles:
                                    timing[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_timings[percent], dtype=np.float), percentille))
                                    duration[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_durations[percent], dtype=np.float), percentille))
                                    freq[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_frequencys[percent], dtype=np.float), percentille))

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

                            current_gauge.winter_highflow_annual()

                            for percent in exceedance_percent:
                                for percentille in percentilles:
                                    timing[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_timings[percent], dtype=np.float), percentille))
                                    duration[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_durations[percent], dtype=np.float), percentille))
                                    freq[percent][percentille].append(np.nanpercentile(np.array(current_gauge.winter_frequencys[percent], dtype=np.float), percentille))

                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')


    column_header = ['Class', 'Gauge #']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in exceedance_percent:
        for percentille in percentilles:
            column_header.append('Timing-{}%_exceedance-{}%'.format(percent, percentille))
            column_header.append('Duration-{}%_exceedance-{}%'.format(percent, percentille))
            column_header.append('Freq-{}%_exceedance-{}%'.format(percent, percentille))

            result_matrix.append(timing[percent][percentille])
            result_matrix.append(duration[percent][percentille])
            result_matrix.append(freq[percent][percentille])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/winter_highflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

    if plot:
        smart_plot(result_matrix)


def winter_highflow_POR(start_date, directoryName, endWith, class_number, gauge_numbers, plot):
    exceedance_percent = [2, 5, 10, 20, 50]
    timing = {}
    duration = {}

    gauges = []

    for i in exceedance_percent:
        timing[i] = []
    for root,dirs,files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):
                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',',
                                       encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df)

                current_gaguge_column_index = 1
                if not class_number and not gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                        current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                        gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                        current_gaguge_column_index = current_gaguge_column_index + step

                elif gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[1, current_gaguge_column_index]) in gauge_numbers:
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                            current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                            gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                            break;

                        current_gaguge_column_index = current_gaguge_column_index + step

                elif class_number:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                            current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                            gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')

    for gauge in gauges:
        if plot:
            gauge.plot_based_on_exceedance()
            gauge.plot_timing()
            gauge.plot_duration()
            gauge.plot_mag()
