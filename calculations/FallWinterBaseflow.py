import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot
from utils.matrix_convert import sort_matrix, insert_column_header

class FallWinterBaseflow(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.wet_baseflows = {}
        for percent in self.percentilles:
            self.wet_baseflows[percent] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.fall_winter_baseflow()

        for percent in self.percentilles:
            self.wet_baseflows[percent].append(np.nanpercentile(current_gauge.wet_baseflows, percent))


    def result_to_csv(self):
        column_header = ['Class', 'Gauge', 'Wet_BFL_Mag_10%', 'Wet_BFL_Mag_50%', 'Wet_BFL_Mag_90%']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percent in self.percentilles:
            result_matrix.append(self.wet_baseflows[percent])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/fall_winter_baseflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
        if self.plot:
            smart_plot(result_matrix)
