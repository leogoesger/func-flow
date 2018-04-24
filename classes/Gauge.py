from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from utils.matrix_convert import insert_column_header
from utils.calc_all_year import calc_all_year
from utils.calc_winter_highflow import calc_winter_highflow_annual, calc_winter_highflow_POR
from utils.calc_spring_transition import calc_spring_transition_timing_magnitude, calc_spring_transition_roc, calc_spring_transition_duration
from utils.calc_summer_baseflow import calc_start_of_summer, calc_summer_baseflow_durations_magnitude
from utils.calc_fall_flush import calc_fall_flush_timings_durations
from utils.calc_fall_winter_baseflow import calc_fall_winter_baseflow
from utils.helpers import remove_offset_from_julian_date
from params import general_params


class Gauge:
    exceedance_percent = [2, 5, 10, 20, 50]

    def __init__(self, class_number, gauge_number, year_ranges, flow_matrix, julian_dates, start_date, start_year, end_year):
        self.class_number = class_number
        self.gauge_number = gauge_number
        self.year_ranges = year_ranges[start_year:end_year]
        self.flow_matrix = flow_matrix[:,start_year:end_year]
        self.julian_dates = julian_dates
        self.start_date = start_date
        self.average_annual_flows = None
        self.standard_deviations = None
        self.coefficient_variations = None
        self.winter_timings = None
        self.winter_durations = None
        self.winter_frequencys = None
        self.winter_timings_POR = None
        self.winter_magnitudes = None
        self.winter_durations_POR = None
        self.winter_frequencys_POR = None
        self.winter_magnitudes_POR = None
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
        average_annual_flows, standard_deviations, coefficient_variations = calc_all_year(self.flow_matrix)
        self.average_annual_flows = np.array(average_annual_flows, dtype=np.float)
        self.standard_deviations = np.array(standard_deviations, dtype=np.float)
        self.coefficient_variations = np.array(coefficient_variations, dtype=np.float)

    def winter_highflow_annual(self):
        winter_timings, winter_durations, winter_frequencys, winter_magnitudes = calc_winter_highflow_annual(
            self.flow_matrix, self.exceedance_percent)
        self.winter_timings = {}
        self.winter_durations = {}
        self.winter_frequencys = {}
        self.winter_magnitudes = {}

        for percent in self.exceedance_percent:
            self.winter_timings[percent] = np.array(winter_timings[percent], dtype=np.float)
            self.winter_durations[percent] = np.array(winter_durations[percent], dtype=np.float)
            self.winter_frequencys[percent] = np.array(winter_frequencys[percent], dtype=np.float)
            self.winter_magnitudes[percent] = np.array(winter_magnitudes[percent], dtype=np.float)

    def winter_highflow_POR(self):
        winter_timings_POR, winter_durations_POR, winter_frequencys_POR, winter_magnitudes_POR = calc_winter_highflow_POR(self.flow_matrix, self.exceedance_percent)

        self.winter_timings_POR = {}
        self.winter_durations_POR = {}
        self.winter_frequencys_POR = {}
        self.winter_magnitudes_POR = {}

        for percent in self.exceedance_percent:
            self.winter_timings_POR[percent] = np.array(winter_timings_POR[percent], dtype=np.float)
            self.winter_durations_POR[percent] = np.array(winter_durations_POR[percent], dtype=np.float)
            self.winter_frequencys_POR[percent] = np.array(winter_frequencys_POR[percent], dtype=np.float)
            self.winter_magnitudes_POR[percent] = np.array(winter_magnitudes_POR[percent], dtype=np.float)

    def spring_transition_timing_magnitude(self):
        spring_timings, spring_magnitudes = calc_spring_transition_timing_magnitude(self.flow_matrix)
        self.spring_timings = np.array(spring_timings, dtype=np.float)
        self.spring_magnitudes = np.array(spring_magnitudes, dtype=np.float)

    def spring_transition_duration(self):
        spring_durations = calc_spring_transition_duration(self.spring_timings, self.summer_timings)
        self.spring_durations = np.array(spring_durations, dtype=np.float)

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
        summer_timings = calc_start_of_summer(self.flow_matrix)
        fall_timings, fall_magnitudes, fall_wet_timings, fall_durations = calc_fall_flush_timings_durations(self.flow_matrix, summer_timings)
        self.fall_timings = np.array(fall_timings, dtype=np.float)
        self.fall_magnitudes = np.array(fall_magnitudes, dtype=np.float)
        self.fall_wet_timings = np.array(fall_wet_timings, dtype=np.float)
        self.fall_durations = np.array(fall_durations, dtype=np.float)

    def fall_winter_baseflow(self):
        self.fall_flush_timings_durations()
        self.spring_transition_timing_magnitude()
        wet_baseflows_10 = calc_fall_winter_baseflow(self.flow_matrix, self.fall_timings, self.fall_wet_timings, self.spring_timings)
        self.wet_baseflows = np.array(wet_baseflows_10, dtype=np.float)

    def create_flow_matrix(self):
        flow_matrix = np.vstack((self.year_ranges, self.flow_matrix))
        np.savetxt("post_processedFiles/Class-{}/{}.csv".format(int(self.class_number), int(self.gauge_number)), flow_matrix, delimiter=",")

    def plot_dates(self):
        def format_func(value, tick_number):
            julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday
            return int(remove_offset_from_julian_date(value, julian_start_date))

        self.start_of_summer()
        self.fall_flush_timings_durations()
        self.spring_transition_timing_magnitude()

        for column_number, flow_data in enumerate(self.flow_matrix[0]):
            flow_data = self.flow_matrix[:, column_number]
            x_axis = list(range(len(flow_data)))

            fig = plt.figure('{}-{}'.format(self.gauge_number, column_number))
            ax = fig.add_subplot(111)
            ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
            ax.plot(x_axis, flow_data)

            if not np.isnan(self.fall_timings[column_number]):
                plt.axvline(self.fall_timings[column_number], ls=":", c="blue")
            if not np.isnan(self.fall_wet_timings[column_number]):
                plt.axvline(self.fall_wet_timings[column_number], ls=":", c="green")
            if not np.isnan(self.spring_timings[column_number]):
                plt.axvline(self.spring_timings[column_number], ls=":", c="orange")
            if not np.isnan(self.summer_timings[column_number]):
                plt.axvline(self.summer_timings[column_number], ls=":", c="red")

            # plt.yscale('log')
            plt.savefig('post_processedFiles/{}-{}.png'.format(self.gauge_number, column_number))

    def create_result_csv(self):
        self.all_year()
        self.start_of_summer()
        self.fall_flush_timings_durations()
        self.summer_baseflow_durations_magnitude()
        self.winter_highflow_annual()
        self.spring_transition_timing_magnitude()
        self.spring_transition_duration()
        self.spring_transition_roc()
        self.fall_winter_baseflow()

        """Convert offset dates to non-offset dates"""
        spring_timings = []
        summer_timings = []
        fall_timings = []
        fall_wet_timings = []
        for index, year in enumerate(self.year_ranges):
            julian_start_date = datetime.strptime("{}/{}".format(self.start_date, year), "%m/%d/%Y").timetuple().tm_yday
            spring_timings.append(remove_offset_from_julian_date(self.spring_timings[index], julian_start_date))
            summer_timings.append(remove_offset_from_julian_date(self.summer_timings[index], julian_start_date))
            fall_timings.append(remove_offset_from_julian_date(self.fall_timings[index], julian_start_date))
            fall_wet_timings.append(remove_offset_from_julian_date(self.fall_wet_timings[index], julian_start_date))

        winter_timings = {}
        for percent in self.exceedance_percent:
            winter_timings[percent] = []
            for index, year in enumerate(self.year_ranges):
                julian_start_date = datetime.strptime("{}/{}".format(self.start_date, year), "%m/%d/%Y").timetuple().tm_yday
                winter_timings[percent].append(remove_offset_from_julian_date(self.winter_timings[percent][index], julian_start_date))


        low_end = general_params['annual_result_low_Percentille_filter']
        high_end = general_params['annual_result_high_Percentille_filter']

        """Filter data only to contain from low_end to high_end"""
        self.average_annual_flows = [np.nan if ele < np.nanpercentile(self.average_annual_flows, low_end) or ele > np.nanpercentile(self.average_annual_flows, high_end) else ele for index, ele in enumerate(self.average_annual_flows)]
        self.standard_deviations = [np.nan if ele < np.nanpercentile(self.standard_deviations, low_end) or ele > np.nanpercentile(self.standard_deviations, high_end) else ele for index, ele in enumerate(self.standard_deviations)]
        self.coefficient_variations = [np.nan if ele < np.nanpercentile(self.coefficient_variations, low_end) or ele > np.nanpercentile(self.coefficient_variations, high_end) else ele for index, ele in enumerate(self.coefficient_variations)]
        spring_timings = [np.nan if ele < np.nanpercentile(spring_timings, low_end) or ele > np.nanpercentile(spring_timings, high_end) else ele for index, ele in enumerate(spring_timings)]
        self.spring_magnitudes = [np.nan if ele < np.nanpercentile(self.spring_magnitudes, low_end) or ele > np.nanpercentile(self.spring_magnitudes, high_end) else ele for index, ele in enumerate(self.spring_magnitudes)]
        self.spring_durations = [np.nan if ele < np.nanpercentile(self.spring_durations, low_end) or ele > np.nanpercentile(self.spring_durations, high_end) else ele for index, ele in enumerate(self.spring_durations)]
        self.spring_rocs = [np.nan if ele < np.nanpercentile(self.spring_rocs, low_end) or ele > np.nanpercentile(self.spring_rocs, high_end) else ele for index, ele in enumerate(self.spring_rocs)]
        summer_timings = [np.nan if ele < np.nanpercentile(summer_timings, low_end) or ele > np.nanpercentile(summer_timings, high_end) else ele for index, ele in enumerate(summer_timings)]
        self.summer_10_magnitudes = [np.nan if ele < np.nanpercentile(self.summer_10_magnitudes, low_end) or ele > np.nanpercentile(self.summer_10_magnitudes, high_end) else ele for index, ele in enumerate(self.summer_10_magnitudes)]
        self.summer_50_magnitudes = [np.nan if ele < np.nanpercentile(self.summer_50_magnitudes, low_end) or ele > np.nanpercentile(self.summer_50_magnitudes, high_end) else ele for index, ele in enumerate(self.summer_50_magnitudes)]
        self.summer_flush_durations = [np.nan if ele < np.nanpercentile(self.summer_flush_durations, low_end) or ele > np.nanpercentile(self.summer_flush_durations, high_end) else ele for index, ele in enumerate(self.summer_flush_durations)]
        self.summer_wet_durations = [np.nan if ele < np.nanpercentile(self.summer_wet_durations, low_end) or ele > np.nanpercentile(self.summer_wet_durations, high_end) else ele for index, ele in enumerate(self.summer_wet_durations)]
        self.summer_no_flow_counts = [np.nan if ele < np.nanpercentile(self.summer_no_flow_counts, low_end) or ele > np.nanpercentile(self.summer_no_flow_counts, high_end) else ele for index, ele in enumerate(self.summer_no_flow_counts)]
        fall_timings = [np.nan if ele < np.nanpercentile(fall_timings, low_end) or ele > np.nanpercentile(fall_timings, high_end) else ele for index, ele in enumerate(fall_timings)]
        self.fall_magnitudes = [np.nan if ele < np.nanpercentile(self.fall_magnitudes, low_end) or ele > np.nanpercentile(self.fall_magnitudes, high_end) else ele for index, ele in enumerate(self.fall_magnitudes)]
        fall_wet_timings = [np.nan if ele < np.nanpercentile(fall_wet_timings, low_end) or ele > np.nanpercentile(fall_wet_timings, high_end) else ele for index, ele in enumerate(fall_wet_timings)]
        self.fall_durations = [np.nan if ele < np.nanpercentile(self.fall_durations, low_end) or ele > np.nanpercentile(self.fall_durations, high_end) else ele for index, ele in enumerate(self.fall_durations)]
        self.wet_baseflows = [np.nan if ele < np.nanpercentile(self.wet_baseflows, low_end) or ele > np.nanpercentile(self.wet_baseflows, high_end) else ele for index, ele in enumerate(self.wet_baseflows)]
        for percent in self.exceedance_percent:
            winter_timings[percent] = [np.nan if ele < np.nanpercentile(winter_timings[percent], low_end) or ele > np.nanpercentile(winter_timings[percent], high_end) else ele for index, ele in enumerate(winter_timings[percent])]
            self.winter_durations[percent] = [np.nan if ele < np.nanpercentile(self.winter_durations[percent], low_end) or ele > np.nanpercentile(self.winter_durations[percent], high_end) else ele for index, ele in enumerate(self.winter_durations[percent])]
            self.winter_frequencys[percent] = [np.nan if ele < np.nanpercentile(self.winter_frequencys[percent], low_end) or ele > np.nanpercentile(self.winter_frequencys[percent], high_end) else ele for index, ele in enumerate(self.winter_frequencys[percent])]
            self.winter_magnitudes[percent] = [np.nan if ele < np.nanpercentile(self.winter_magnitudes[percent], low_end) or ele > np.nanpercentile(self.winter_magnitudes[percent], high_end) else ele for index, ele in enumerate(self.winter_magnitudes[percent])]

        """result to CSV"""
        result_matrix = []
        result_matrix.append(self.year_ranges)
        result_matrix.append(self.average_annual_flows)
        result_matrix.append(self.standard_deviations)
        result_matrix.append(self.coefficient_variations)
        result_matrix.append(spring_timings)
        result_matrix.append(self.spring_magnitudes)
        result_matrix.append(self.spring_durations)
        result_matrix.append(self.spring_rocs)
        result_matrix.append(summer_timings)
        result_matrix.append(self.summer_10_magnitudes)
        result_matrix.append(self.summer_50_magnitudes)
        result_matrix.append(self.summer_flush_durations)
        result_matrix.append(self.summer_wet_durations)
        result_matrix.append(self.summer_no_flow_counts)
        result_matrix.append(fall_timings)
        result_matrix.append(self.fall_magnitudes)
        result_matrix.append(fall_wet_timings)
        result_matrix.append(self.fall_durations)
        result_matrix.append(self.wet_baseflows)
        for percent in self.exceedance_percent:
            result_matrix.append(winter_timings[percent])
            result_matrix.append(self.winter_durations[percent])
            result_matrix.append(self.winter_frequencys[percent])
            result_matrix.append(self.winter_magnitudes[percent])

        column_header = ['Year', 'Avg', 'Std', 'CV', 'SP_Tim', 'SP_Mag', 'SP_Dur', 'SP_ROC', 'SU_BFL_Tim', 'SU_BFL_Mag_10', 'SU_BFL_Mag_50', 'SU_BFL_Dur_Fl', 'SU_BFL_Dur_Wet', 'SU_BFL_No_Flow', 'FAFL_Tim', 'FAFL_Mag', 'FAFL_Tim_Wet', 'FAFL_Dur', 'Wet_BFL_Mag', 'WIN_Tim_2', 'WIN_Dur_2', 'WIN_Fre_2', 'WIN_Mag_2', 'WIN_Tim_5', 'WIN_Dur_5', 'WIN_Fre_5', 'WIN_Mag_5', 'WIN_Tim_10', 'WIN_Dur_10', 'WIN_Fre_10', 'WIN_Mag_10', 'WIN_Tim_20', 'WIN_Dur_20', 'WIN_Fre_20', 'WIN_Mag_20', 'WIN_Tim_50', 'WIN_Dur_50', 'WIN_Fre_50', 'WIN_Mag_50']

        # column_header = ['Year', 'Avg', 'Std', 'CV', 'SP_Tim', 'SP_Mag', 'SP_Dur', 'SP_ROC', 'SU_Tim', 'SU_Mag_10', 'SU_Mag_50', 'SU_Dur_Fl', 'SU_Dur_Wet', 'SU_No_Flow', 'FA_Tim', 'FA_Mag', 'FA_Tim_Wet', 'FA_Dur', 'Wet_BFL_Mag', 'Tim_2', 'Dur_2', 'Fre_2', 'Mag_2', 'Tim_5', 'Dur_5', 'Fre_5', 'Mag_5','Tim_10', 'Dur_10', 'Fre_10', 'Mag_10', 'Tim_20', 'Dur_20', 'Fre_20', 'Mag_20', 'Tim_50', 'Dur_50', 'Fre_50', 'Mag_50']

        new_result_matrix = []
        for index, row in enumerate(result_matrix):
            new_result_matrix.append(list(result_matrix[index]))

        if len(new_result_matrix) == len(column_header):
            new_result_matrix = insert_column_header(new_result_matrix, column_header)
        else:
            print('Column header does not have the same dimension as result matrix')

        np.savetxt("post_processedFiles/{}_annual_result_matrix.csv".format(
            int(self.gauge_number)), new_result_matrix, delimiter=",", fmt="%s")
