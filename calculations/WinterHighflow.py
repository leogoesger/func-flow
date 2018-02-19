from datetime import datetime
import os
import numpy as np
import pandas as pd
from classes.Abstract import Abstract
from utils.helpers import smart_plot, remove_offset_from_julian_date, is_multiple_date_data
from utils.matrix_convert import sort_matrix, insert_column_header, convert_raw_data_to_matrix
from utils.calc_winter_highflow import calc_winter_highflow_POR
from classes.GaugePlotter import GaugePlotter


class WinterHighflow(Abstract):
    exceedance_percent = [2, 5, 10, 20, 50]

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()
        self.julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.timing = {}
        self.duration = {}
        self.freq = {}

        for percent in self.exceedance_percent:
            self.timing[percent] = {}
            self.duration[percent] = {}
            self.freq[percent] = {}
            for percentille in self.percentilles:
                self.timing[percent][percentille] = []
                self.duration[percent][percentille] = []
                self.freq[percent][percentille] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.winter_highflow_annual()

        for percent in self.exceedance_percent:
            for percentille in self.percentilles:
                current_gauge_winter_timing = np.nanpercentile(current_gauge.winter_timings[percent], percentille)
                current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, self.julian_start_date)

                self.timing[percent][percentille].append(current_gauge_winter_timing)
                self.duration[percent][percentille].append(np.nanpercentile(current_gauge.winter_durations[percent], percentille))
                self.freq[percent][percentille].append(np.nanpercentile(current_gauge.winter_frequencys[percent], percentille))

    def result_to_csv(self):
        column_header = ['Class', 'Gauge #']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percent in self.exceedance_percent:
            for percentille in self.percentilles:
                column_header.append('WIN_Tim_{}_{}'.format(percent, percentille))
                column_header.append('WIN_Dur_{}_{}'.format(percent, percentille))
                column_header.append('WIN_Fre_{}_{}'.format(percent, percentille))

                result_matrix.append(self.timing[percent][percentille])
                result_matrix.append(self.duration[percent][percentille])
                result_matrix.append(self.freq[percent][percentille])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/winter_highflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

        if self.plot:
            smart_plot(result_matrix)

def winter_highflow_POR(start_date, directory_name, end_with, class_number, gauge_numbers, plot):
    exceedance_percent = [2, 5, 10, 20, 50]
    percentilles = [10, 50, 90]
    julian_start_date = datetime.strptime("{}/2001".format(start_date), "%m/%d/%Y").timetuple().tm_yday

    gauges = []
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

    for root,dirs,files in os.walk(directory_name):
        for file in files:
            if file.endswith(end_with):
                fixed_df = pd.read_csv('{}/{}'.format(directory_name, file), sep=',',
                                       encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df)

                current_gauge_column_index = 1
                if not class_number and not gauge_numbers:
                    while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                        """General Info"""
                        gauge_class_array.append(current_gauge_class)
                        gauge_number_array.append(current_gauge_number)

                        current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                        gauges.append(GaugePlotter(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                        for percent in exceedance_percent:
                            for percentille in percentilles:
                                current_gauge_winter_timing = np.nanpercentile(current_timing[percent], percentille)
                                current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, julian_start_date)

                                timing[percent][percentille].append(current_gauge_winter_timing)
                                duration[percent][percentille].append(np.nanpercentile(current_duration[percent], percentille))
                                freq[percent][percentille].append(np.nanpercentile(current_freq[percent], percentille))

                        current_gauge_column_index = current_gauge_column_index + step

                elif gauge_numbers:
                    while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[1, current_gauge_column_index]) in gauge_numbers:
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                            gauges.append(GaugePlotter(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                            for percent in exceedance_percent:
                                for percentille in percentilles:
                                    current_gauge_winter_timing = np.nanpercentile(current_timing[percent], percentille)
                                    current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, julian_start_date)

                                    timing[percent][percentille].append(current_gauge_winter_timing)
                                    duration[percent][percentille].append(np.nanpercentile(current_duration[percent], percentille))
                                    freq[percent][percentille].append(np.nanpercentile(current_freq[percent], percentille))

                            break;

                        current_gauge_column_index = current_gauge_column_index + step

                elif class_number:
                    while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[0, current_gauge_column_index]) == int(class_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date)

                            """General Info"""
                            gauge_class_array.append(current_gauge_class)
                            gauge_number_array.append(current_gauge_number)

                            current_timing, current_duration, current_freq, current_magnitude = calc_winter_highflow_POR(flow_matrix, exceedance_percent)

                            gauges.append(GaugePlotter(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                            for percent in exceedance_percent:
                                for percentille in percentilles:
                                    current_gauge_winter_timing = np.nanpercentile(current_timing[percent], percentille)
                                    current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, julian_start_date)

                                    timing[percent][percentille].append(current_gauge_winter_timing)
                                    duration[percent][percentille].append(np.nanpercentile(current_duration[percent], percentille))
                                    freq[percent][percentille].append(np.nanpercentile(current_freq[percent], percentille))

                        current_gauge_column_index = current_gauge_column_index + step

                else:
                    print('Something went wrong!')

    column_header = ['Class', 'Gauge #']
    result_matrix = []
    result_matrix.append(gauge_class_array)
    result_matrix.append(gauge_number_array)

    for percent in exceedance_percent:
        for percentille in percentilles:
            column_header.append('WIN_Tim_{}_{}'.format(percent, percentille))
            column_header.append('WIN_Dur_{}_{}'.format(percent, percentille))
            column_header.append('WIN_Fre_{}_{}'.format(percent, percentille))

            result_matrix.append(timing[percent][percentille])
            result_matrix.append(duration[percent][percentille])
            result_matrix.append(freq[percent][percentille])

    result_matrix = sort_matrix(result_matrix, 0)
    result_matrix = insert_column_header(result_matrix, column_header)

    np.savetxt("post_processedFiles/winter_highflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

    if plot:
        smart_plot(result_matrix)

    # for gauge in gauges:
    #     if plot:
    #         gauge.plot_based_on_exceedance()
    #         gauge.plot_timing()
    #         gauge.plot_duration()
    #         gauge.plot_mag()
