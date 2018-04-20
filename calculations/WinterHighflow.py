from datetime import datetime
import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot, remove_offset_from_julian_date, nonP_box_plot
from utils.matrix_convert import sort_matrix, insert_column_header
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
        self.mag = {}

        for percent in self.exceedance_percent:
            self.timing[percent] = {}
            self.duration[percent] = {}
            self.freq[percent] = {}
            self.mag[percent] = {}
            for percentille in self.percentilles:
                self.timing[percent][percentille] = []
                self.duration[percent][percentille] = []
                self.freq[percent][percentille] = []
                self.mag[percent][percentille] = []

        self.metrics = {'WIN_Tim_2':{},'WIN_Dur_2':{},'WIN_Fre_2':{},'WIN_Mag_2':{}, 'WIN_Tim_5':{},'WIN_Dur_5':{},'WIN_Fre_5':{},'WIN_Mag_5':{}, 'WIN_Tim_10':{},'WIN_Dur_10':{},'WIN_Fre_10':{}, 'WIN_Mag_10':{},'WIN_Tim_20':{},'WIN_Dur_20':{},'WIN_Fre_20':{},'WIN_Mag_20':{},'WIN_Tim_50':{},'WIN_Dur_50':{},'WIN_Fre_50':{}, 'WIN_Mag_50':{}}

        for key in self.metrics:
            for number in range(1,10):
                self.metrics[key][number] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.winter_highflow_annual()

        """Remove offset"""
        for percent in self.exceedance_percent:
            for percentille in self.percentilles:
                current_gauge_winter_timing = np.nanpercentile(current_gauge.winter_timings[percent], percentille)
                current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, self.julian_start_date)

                self.timing[percent][percentille].append(current_gauge_winter_timing)
                self.duration[percent][percentille].append(np.nanpercentile(current_gauge.winter_durations[percent], percentille))
                self.freq[percent][percentille].append(np.nanpercentile(current_gauge.winter_frequencys[percent], percentille))
                self.mag[percent][percentille].append(np.nanpercentile(current_gauge.winter_magnitudes[percent], percentille))

        """Get nonP result"""
        for percent in self.exceedance_percent:
            self.metrics['WIN_Tim_{}'.format(percent)][current_gauge.class_number] += list(current_gauge.winter_timings[percent])
            self.metrics['WIN_Dur_{}'.format(percent)][current_gauge.class_number] += list(current_gauge.winter_durations[percent])
            self.metrics['WIN_Fre_{}'.format(percent)][current_gauge.class_number] += list(current_gauge.winter_frequencys[percent])
            self.metrics['WIN_Mag_{}'.format(percent)][current_gauge.class_number] += list(current_gauge.winter_magnitudes[percent])

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
                column_header.append('WIN_Mag_{}_{}'.format(percent, percentille))

                result_matrix.append(self.timing[percent][percentille])
                result_matrix.append(self.duration[percent][percentille])
                result_matrix.append(self.freq[percent][percentille])
                result_matrix.append(self.mag[percent][percentille])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/winter_highflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

        if self.plot:
            smart_plot(result_matrix)

        """nonP plots"""
        WIN_Tim_2 = []
        WIN_Dur_2 = []
        WIN_Fre_2 = []
        WIN_Mag_2 = []
        WIN_Tim_5 = []
        WIN_Dur_5 = []
        WIN_Fre_5 = []
        WIN_Mag_5 = []
        WIN_Tim_10 = []
        WIN_Dur_10 = []
        WIN_Fre_10 = []
        WIN_Mag_10 = []
        WIN_Tim_20 = []
        WIN_Dur_20 = []
        WIN_Fre_20 = []
        WIN_Mag_20 = []
        WIN_Tim_50 = []
        WIN_Dur_50 = []
        WIN_Fre_50 = []
        WIN_Mag_50 = []

        for class_id in range(1,10):
            WIN_Tim_2.append(self.metrics['WIN_Tim_2'][class_id])
            WIN_Dur_2.append(self.metrics['WIN_Dur_2'][class_id])
            WIN_Fre_2.append(self.metrics['WIN_Fre_2'][class_id])
            WIN_Fre_2.append(self.metrics['WIN_Mag_2'][class_id])
            WIN_Tim_5.append(self.metrics['WIN_Tim_5'][class_id])
            WIN_Dur_5.append(self.metrics['WIN_Dur_5'][class_id])
            WIN_Fre_5.append(self.metrics['WIN_Fre_5'][class_id])
            WIN_Fre_5.append(self.metrics['WIN_Mag_5'][class_id])
            WIN_Tim_10.append(self.metrics['WIN_Tim_10'][class_id])
            WIN_Dur_10.append(self.metrics['WIN_Dur_10'][class_id])
            WIN_Fre_10.append(self.metrics['WIN_Fre_10'][class_id])
            WIN_Fre_10.append(self.metrics['WIN_Mag_10'][class_id])
            WIN_Tim_20.append(self.metrics['WIN_Tim_20'][class_id])
            WIN_Dur_20.append(self.metrics['WIN_Dur_20'][class_id])
            WIN_Fre_20.append(self.metrics['WIN_Fre_20'][class_id])
            WIN_Fre_20.append(self.metrics['WIN_Mag_20'][class_id])
            WIN_Tim_50.append(self.metrics['WIN_Tim_50'][class_id])
            WIN_Dur_50.append(self.metrics['WIN_Dur_50'][class_id])
            WIN_Fre_50.append(self.metrics['WIN_Fre_50'][class_id])
            WIN_Fre_50.append(self.metrics['WIN_Mag_50'][class_id])

        combined = {'WIN_Tim_2': WIN_Tim_2, 'WIN_Dur_2': WIN_Dur_2, 'WIN_Fre_2': WIN_Fre_2,'WIN_Mag_2': WIN_Mag_2, 'WIN_Tim_5': WIN_Tim_5, 'WIN_Dur_5': WIN_Dur_5, 'WIN_Fre_5': WIN_Fre_5,'WIN_Mag_5': WIN_Mag_5,'WIN_Tim_10': WIN_Tim_10, 'WIN_Dur_10': WIN_Dur_10, 'WIN_Fre_10': WIN_Fre_10,'WIN_Mag_10': WIN_Mag_10,'WIN_Tim_20': WIN_Tim_20, 'WIN_Dur_20': WIN_Dur_20, 'WIN_Fre_20': WIN_Fre_20,'WIN_Mag_20': WIN_Mag_20,'WIN_Tim_50': WIN_Tim_50, 'WIN_Dur_50': WIN_Dur_50, 'WIN_Fre_50': WIN_Fre_50, 'WIN_Mag_50': WIN_Mag_50}

        if self.plot:
            nonP_box_plot(combined)

class WinterHighflowPOR(Abstract):
    exceedance_percent = [2, 5, 10, 20, 50]

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()
        self.julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday

    def _prepare_result_arrays(self):
        self.gauges = []
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
        current_gauge.winter_highflow_POR()

        self.gauges.append(GaugePlotter(self.gauge_class_array[-1], self.gauge_number_array[-1], current_gauge.winter_timings_POR, current_gauge.winter_durations_POR, current_gauge.winter_frequencys_POR, current_gauge.winter_magnitudes_POR, self.exceedance_percent))

        for percent in self.exceedance_percent:
            for percentille in self.percentilles:
                current_gauge_winter_timing = np.nanpercentile(current_gauge.winter_timings_POR[percent], percentille)
                current_gauge_winter_timing = remove_offset_from_julian_date(current_gauge_winter_timing, self.julian_start_date)

                self.timing[percent][percentille].append(current_gauge_winter_timing)
                self.duration[percent][percentille].append(np.nanpercentile(current_gauge.winter_durations_POR[percent], percentille))
                self.freq[percent][percentille].append(np.nanpercentile(current_gauge.winter_frequencys_POR[percent], percentille))

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

        np.savetxt("post_processedFiles/winter_highflow_POR_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

        # if self.plot:
        #     smart_plot(result_matrix)

        for gauge in self.gauges:
            if self.plot:
                gauge.plot_based_on_exceedance()
                gauge.plot_timing()
                gauge.plot_duration()
                gauge.plot_mag()
