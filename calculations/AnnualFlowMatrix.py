from classes.Abstract import Abstract

class AnnualFlowMatrix(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self._prepare_result_arrays()

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.create_result_csv()
        # current_gauge.create_flow_matrix()
        current_gauge.plot_dates()

    def result_to_csv(self):
        return None
