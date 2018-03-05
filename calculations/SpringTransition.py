from datetime import datetime
import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot, remove_offset_from_julian_date, nonP_box_plot
from utils.matrix_convert import sort_matrix, insert_column_header

class SpringTransition(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()
        self.julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.spring_timings = {}
        self.spring_durations = {}
        self.spring_magnitudes = {}
        self.spring_rocs = {}

        for percent in self.percentilles:
            self.spring_timings[percent] = []
            self.spring_durations[percent] = []
            self.spring_magnitudes[percent] = []
            self.spring_rocs[percent] = []

        self.metrics = {'SP_Tim':{},'SP_Mag':{},'SP_Dur':{},'SP_ROC':{}}
        for key in self.metrics:
            for number in range(1,10):
                self.metrics[key][number] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.spring_transition_timing_magnitude()
        current_gauge.start_of_summer()
        current_gauge.spring_transition_duration()
        current_gauge.spring_transition_roc()

        """Remove offset"""
        for percent in self.percentilles:
            current_gauge_spring_timing = np.nanpercentile(current_gauge.spring_timings, percent)
            current_gauge_spring_timing = remove_offset_from_julian_date(current_gauge_spring_timing, self.julian_start_date)

            self.spring_timings[percent].append(current_gauge_spring_timing)
            self.spring_durations[percent].append(np.nanpercentile(current_gauge.spring_durations, percent))
            self.spring_magnitudes[percent].append(np.nanpercentile(current_gauge.spring_magnitudes, percent))
            self.spring_rocs[percent].append(np.nanpercentile(current_gauge.spring_rocs, percent))

        """Get nonP result"""
        self.metrics['SP_Tim'][self.gauge_class_array[-1]] += list(current_gauge.spring_timings)
        self.metrics['SP_Mag'][self.gauge_class_array[-1]] += list(current_gauge.spring_magnitudes)
        self.metrics['SP_Dur'][self.gauge_class_array[-1]] += list(current_gauge.spring_durations)
        self.metrics['SP_ROC'][self.gauge_class_array[-1]] += list(current_gauge.spring_rocs)

    def result_to_csv(self):
        column_header = ['Class', 'Gauge', 'SP_Tim_10', 'SP_Dur_10', 'SP_Mag_10', 'SP_ROC_10', 'SP_Tim_50', 'SP_Dur_50', 'SP_Mag_50', 'SP_ROC_50', 'SP_Tim_90', 'SP_Dur_90', 'SP_Mag_90', 'SP_ROC_90']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percent in self.percentilles:
            result_matrix.append(self.spring_timings[percent])
            result_matrix.append(self.spring_durations[percent])
            result_matrix.append(self.spring_magnitudes[percent])
            result_matrix.append(self.spring_rocs[percent])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/spring_transition_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
        if self.plot:
            smart_plot(result_matrix)

        """nonP plots"""
        SP_Tim = []
        SP_Mag = []
        SP_Dur = []
        SP_ROC = []

        for class_id in range(1,10):
            SP_Tim.append(self.metrics['SP_Tim'][class_id])
            SP_Mag.append(self.metrics['SP_Mag'][class_id])
            SP_Dur.append(self.metrics['SP_Dur'][class_id])
            SP_ROC.append(self.metrics['SP_ROC'][class_id])

        combined = {'SP_Tim': SP_Tim, 'SP_Mag': SP_Mag, 'SP_Dur': SP_Dur, 'SP_ROC': SP_ROC}
        if self.plot:
            nonP_box_plot(combined)
