import numpy as np
from utils.matrix_convert import insert_column_header
from utils.calc_winter_highflow_properties import calculate_timing_duration_frequency_annual
from utils.calc_summer_baseflow import calc_start_of_summer


class Gauge:
    exceedance_percent = [2, 5, 10, 20, 50]
    start_date_for_summer_calc = '1/1'

    def __init__(self, class_number, gauge_number, year_ranges, flow_matrix, julian_dates, start_date):
        self.class_number = class_number
        self.gauge_number = gauge_number
        self.year_ranges = year_ranges
        self.flow_matrix = flow_matrix
        self.julian_dates = julian_dates
        self.start_date = start_date
        self.average = []
        self.std = []
        self.cov = []
        self.timing = None
        self.duration = None
        self.frequency = None
        self.sos = None

    def cov_each_column(self):
        for index, flow in enumerate(self.flow_matrix[0]):
            self.average.append(np.nanmean(self.flow_matrix[:, index]))
            self.std.append(np.nanstd(self.flow_matrix[:, index]))
            self.cov.append(self.std[-1] / self.average[-1])

    def timing_duration_frequency(self):
        self.timing, self.duration, self.frequency = calculate_timing_duration_frequency_annual(
            self.flow_matrix, self.year_ranges, self.start_date, self.exceedance_percent)

    def start_of_summer(self):
        self.sos = calc_start_of_summer(
            self.flow_matrix, self.start_date_for_summer_calc)

    def create_result_csv(self):
        result_matrix = []
        result_matrix.append(self.year_ranges)
        result_matrix.append(self.average)
        result_matrix.append(self.std)
        result_matrix.append(self.cov)
        for percent in self.exceedance_percent:
            result_matrix.append(self.timing[percent])
            result_matrix.append(self.duration[percent])
            result_matrix.append(self.frequency[percent])
        result_matrix.append(self.sos)

        column_header = ['Year', 'Avg', 'Std', 'CV', 'Tim_2', 'Dur_2', 'Fre_2', 'Tim_5', 'Dur_5', 'Fre_5',
                         'Tim_10', 'Dur_10', 'Fre_10', 'Tim_20', 'Dur_20', 'Fre_20', 'Tim_50', 'Dur_50', 'Fre_50', 'SOS']

        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/{}_annual_result_matrix.csv".format(
            int(self.gauge_number)), result_matrix, delimiter=",", fmt="%s")
