import numpy as np
import matplotlib.pyplot as plt
from utils.matrix_convert import insert_column_header
from utils.calc_winter_highflow import calc_winter_highflow_annual
from utils.calc_spring_transition import calc_spring_transition_timing_magnitude, calc_spring_transition_roc
from utils.calc_summer_baseflow import calc_start_of_summer, calc_summer_baseflow_durations_magnitude
from utils.calc_fall_flush import calc_fall_flush_timings_durations
from utils.calc_fall_winter_baseflow import calc_fall_winter_baseflow

class Gauge:
    exceedance_percent = [2, 5, 10, 20, 50]

    def __init__(self, class_number, gauge_number, year_ranges, flow_matrix, julian_dates, start_date):
        self.class_number = class_number
        self.gauge_number = gauge_number
        self.year_ranges = year_ranges
        self.flow_matrix = flow_matrix
        self.julian_dates = julian_dates
        self.start_date = start_date
        self.average_annual_flows = None
        self.standard_deviations = None
        self.coefficient_variations = None
        self.winter_timings = None
        self.winter_durations = None
        self.winter_frequencys = None
        self.spring_timings = None
        self.spring_magnitudes = None
        self.spring_durations = None
        self.spring_rocs = None
        self.summer_timings = None
        self.summer_10_magnitudes = None
        self.summer_50_magnitudes = None
        self.summer_flush_durations = None
        self.summer_wet_durations = None
        self.summer_no_flow_counts = None
        self.fall_timings = None
        self.fall_magnitudes = None
        self.fall_durations = None
        self.fall_wet_timings = None
        self.wet_baseflows = None

    def all_year(self):
        average_annual_flows = []
        standard_deviations = []
        coefficient_variations = []
        for index, flow in enumerate(self.flow_matrix[0]):
            average_annual_flows.append(np.nanmean(self.flow_matrix[:, index]))
            standard_deviations.append(np.nanstd(self.flow_matrix[:, index]))
            coefficient_variations.append(standard_deviations[-1] / average_annual_flows[-1])
        self.average_annual_flows = np.array(average_annual_flows, dtype=np.float)
        self.standard_deviations = np.array(standard_deviations, dtype=np.float)
        self.coefficient_variations = np.array(coefficient_variations, dtype=np.float)

    def winter_highflow_annual(self):
        self.winter_timings, self.winter_durations, self.winter_frequencys = calc_winter_highflow_annual(
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

    def summer_baseflow_durations_magnitude(self):
        summer_10_magnitudes, summer_50_magnitudes, summer_flush_durations, summer_wet_durations, summer_no_flow_counts = calc_summer_baseflow_durations_magnitude(self.flow_matrix, self.summer_timings, self.fall_timings, self.fall_wet_timings)
        self.summer_10_magnitudes = np.array(summer_10_magnitudes, dtype=np.float)
        self.summer_50_magnitudes = np.array(summer_50_magnitudes, dtype=np.float)
        self.summer_flush_durations = np.array(summer_flush_durations, dtype=np.float)
        self.summer_wet_durations = np.array(summer_wet_durations, dtype=np.float)
        self.summer_no_flow_counts = np.array(summer_no_flow_counts, dtype=np.float)

    def fall_flush_timings_durations(self):
        fall_timings, fall_magnitudes, fall_wet_timings, fall_durations = calc_fall_flush_timings_durations(self.flow_matrix)
        self.fall_timings = np.array(fall_timings, dtype=np.float)
        self.fall_magnitudes = np.array(fall_magnitudes, dtype=np.float)
        self.fall_wet_timings = np.array(fall_wet_timings, dtype=np.float)
        self.fall_durations = np.array(fall_durations, dtype=np.float)

    def fall_winter_baseflow(self):
        wet_baseflows_10 = calc_fall_winter_baseflow(self.flow_matrix, self.fall_timings, self.fall_wet_timings, self.spring_timings)
        self.wet_baseflows = np.array(wet_baseflows_10, dtype=np.float)

    def create_flow_matrix(self):
        flow_matrix = np.vstack((self.year_ranges, self.flow_matrix))
        np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(self.class_number), int(self.gauge_number)), flow_matrix, delimiter=",")

    def plot_dates(self):
        self.start_of_summer()
        self.fall_flush_timings_durations()
        self.spring_transition_timing_magnitude()

        print(self.fall_timings)
        for column_number, flow_data in enumerate(self.flow_matrix[0]):
            flow_data = self.flow_matrix[:, column_number]
            x_axis = list(range(len(flow_data)))

            plt.figure('{}-{}'.format(self.gauge_number, column_number))
            plt.plot(x_axis, flow_data)

            if not np.isnan(self.fall_timings[column_number]):
                plt.axvline(self.fall_timings[column_number], ls=":", c="blue")
            if not np.isnan(self.fall_wet_timings[column_number]):
                plt.axvline(self.fall_wet_timings[column_number], ls=":", c="green")
            if not np.isnan(self.spring_timings[column_number]):
                plt.axvline(self.spring_timings[column_number], ls=":", c="orange")
            if not np.isnan(self.summer_timings[column_number]):
                plt.axvline(self.summer_timings[column_number], ls=":", c="red")

            plt.savefig('post_processedFiles/{}-{}.png'.format(self.gauge_number, column_number))

    def create_result_csv(self):
        result_matrix = []
        result_matrix.append(self.year_ranges)
        result_matrix.append(self.average_annual_flows)
        result_matrix.append(self.standard_deviations)
        result_matrix.append(self.coefficient_variations)
        result_matrix.append(self.spring_timings)
        result_matrix.append(self.spring_magnitudes)
        result_matrix.append(self.spring_durations)
        result_matrix.append(self.spring_rocs)
        result_matrix.append(self.summer_timings)
        result_matrix.append(self.fall_timings)
        result_matrix.append(self.fall_magnitudes)
        result_matrix.append(self.fall_durations)
        result_matrix.append(self.fall_wet_timings)
        for percent in self.exceedance_percent:
            result_matrix.append(self.winter_timings[percent])
            result_matrix.append(self.winter_durations[percent])
            result_matrix.append(self.winter_frequencys[percent])

        column_header = ['Year', 'Avg', 'Std', 'CV', 'SP_Tim', 'SP_Mag', 'SP_Dur', 'SP_ROC', 'SU_Tim', 'FA_Tim', 'FA_Mag', 'FA_Dur', 'FA_Tim_Wet', 'Tim_2', 'Dur_2', 'Fre_2', 'Tim_5', 'Dur_5', 'Fre_5','Tim_10', 'Dur_10', 'Fre_10', 'Tim_20', 'Dur_20', 'Fre_20', 'Tim_50', 'Dur_50', 'Fre_50']

        new_result_matrix = []
        for index, row in enumerate(result_matrix):
            new_result_matrix.append(list(result_matrix[index]))

        if len(new_result_matrix) == len(column_header):
            new_result_matrix = insert_column_header(new_result_matrix, column_header)
        else:
            print('Column header does not have the same dimension as result matrix')

        np.savetxt("post_processedFiles/{}_annual_result_matrix.csv".format(
            int(self.gauge_number)), new_result_matrix, delimiter=",", fmt="%s")
