import numpy as np
from utils.matrix_convert import insert_column_header
from utils.calc_winter_highflow import calculate_timing_duration_frequency_annual
from utils.calc_spring_transition import calc_spring_transition_timing_magnitude, calc_spring_transition_roc
from utils.calc_summer_baseflow import calc_start_of_summer
from utils.calc_fall_flush import calc_fall_flush_timings, calc_fall_flush_durations

class Gauge:
    exceedance_percent = [2, 5, 10, 20, 50]

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
        self.winter_timings = None
        self.winter_durations = None
        self.winter_frequencys = None
        self.spring_timings = None
        self.spring_magnitudes = None
        self.spring_durations = None
        self.spring_rocs = None
        self.summer_timings = None
        self.fall_timings = None
        self.fall_magnitudes = None
        self.fall_durations = None
        self.fall_wet_timings = None

    def cov_each_column(self):
        for index, flow in enumerate(self.flow_matrix[0]):
            self.average.append(np.nanmean(self.flow_matrix[:, index]))
            self.std.append(np.nanstd(self.flow_matrix[:, index]))
            self.cov.append(self.std[-1] / self.average[-1])

    def timing_duration_frequency(self):
        self.winter_timings, self.winter_durations, self.winter_frequencys = calculate_timing_duration_frequency_annual(
            self.flow_matrix, self.year_ranges, self.start_date, self.exceedance_percent)

    def spring_transition_timing_magnitude(self):
        spring_timings, spring_magnitudes = calc_spring_transition_timing_magnitude(self.flow_matrix)
        self.spring_timings = np.array(spring_timings, dtype=np.float)
        self.spring_magnitudes = np.array(spring_magnitudes, dtype=np.float)

    def spring_transition_duration(self):
        duration_array = []
        for index, spring_timing in enumerate(self.spring_timings):
            if spring_timing and self.summer_timings[index] and self.summer_timings[index] > spring_timing:
                duration_array.append(self.summer_timings[index] - spring_timing)
            else:
                duration_array.append(None)
        self.spring_durations = np.array(duration_array, dtype=np.float)

    def spring_transition_roc(self):
        spring_rocs = calc_spring_transition_roc(self.flow_matrix, self.spring_timings, self.summer_timings)
        self.spring_rocs = np.array(spring_rocs, dtype=np.float)

    def start_of_summer(self):
        summer_timings = calc_start_of_summer(self.flow_matrix)
        self.summer_timings = np.array(summer_timings, dtype=np.float)

    def fall_flush_timings(self):
        fall_timings, fall_wet_timings = calc_fall_flush_timings(self.flow_matrix)
        self.fall_timings = np.array(fall_timings, dtype=np.float)
        self.fall_wet_timings = np.array(fall_wet_timings, dtype=np.float)

    def fall_flush_durations(self):
        fall_flush_durations = calc_fall_flush_durations(self.flow_matrix, self.fall_timings)
        self.fall_durations = np.array(fall_flush_durations, dtype=np.float)

    def create_result_csv(self):
        result_matrix = []
        result_matrix.append(self.year_ranges)
        result_matrix.append(self.average)
        result_matrix.append(self.std)
        result_matrix.append(self.cov)
        for percent in self.exceedance_percent:
            result_matrix.append(self.winter_timings[percent])
            result_matrix.append(self.winter_durations[percent])
            result_matrix.append(self.winter_frequencys[percent])
        result_matrix.append(self.summer_timings)

        column_header = ['Year', 'Avg', 'Std', 'CV', 'Tim_2', 'Dur_2', 'Fre_2', 'Tim_5', 'Dur_5', 'Fre_5','Tim_10', 'Dur_10', 'Fre_10', 'Tim_20', 'Dur_20', 'Fre_20', 'Tim_50', 'Dur_50', 'Fre_50', 'SOS']

        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/{}_annual_result_matrix.csv".format(
            int(self.gauge_number)), result_matrix, delimiter=",", fmt="%s")
