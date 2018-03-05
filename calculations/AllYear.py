import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot, nonP_box_plot
from utils.matrix_convert import sort_matrix, insert_column_header

class AllYear(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.average_annual_flows = {}
        self.standard_deviations = {}
        self.coefficient_variations = {}

        for percent in self.percentilles:
            self.average_annual_flows[percent] = []
            self.standard_deviations[percent] = []
            self.coefficient_variations[percent] = []

        self.metrics = {'Avg':{},'Std':{},'CV':{}}
        for key in self.metrics:
            for number in range(1,10):
                self.metrics[key][number] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.all_year()

        for percent in self.percentilles:
            self.average_annual_flows[percent].append(np.nanpercentile(current_gauge.average_annual_flows, percent))
            self.standard_deviations[percent].append(np.nanpercentile(current_gauge.standard_deviations, percent))
            self.coefficient_variations[percent].append(np.nanpercentile(current_gauge.coefficient_variations, percent))

        """Get nonP result"""
        self.metrics['Avg'][current_gauge.class_number] += list(current_gauge.average_annual_flows)
        self.metrics['Std'][current_gauge.class_number] += list(current_gauge.standard_deviations)
        self.metrics['CV'][current_gauge.class_number] += list(current_gauge.coefficient_variations)

    def result_to_csv(self):
        column_header = ['Class', 'Gauge', 'Avg_10%', 'Std_10%', 'CV_10%', 'Avg_50%', 'Std_50%', 'CV_50%', 'Avg_90%', 'Std_90%', 'CV_90%']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percent in self.percentilles:
            result_matrix.append(self.average_annual_flows[percent])
            result_matrix.append(self.standard_deviations[percent])
            result_matrix.append(self.coefficient_variations[percent])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/all_year_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")

        if self.plot:
            smart_plot(result_matrix)

        """nonP plots"""
        Avg = []
        Std = []
        CV = []

        for class_id in range(1,10):
            Avg.append(self.metrics['Avg'][class_id])
            Std.append(self.metrics['Std'][class_id])
            CV.append(self.metrics['CV'][class_id])

        combined = {'Avg': Avg, 'Std': Std, 'CV': CV}
        if self.plot:
            nonP_box_plot(combined)
