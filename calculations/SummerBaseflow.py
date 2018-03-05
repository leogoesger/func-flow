from datetime import datetime
import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot, remove_offset_from_julian_date, nonP_box_plot
from utils.matrix_convert import sort_matrix, insert_column_header

class SummerBaseflow(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()
        self.julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.summer_timings = {}
        self.summer_10_magnitudes = {}
        self.summer_50_magnitudes = {}
        self.summer_flush_durations = {}
        self.summer_wet_durations = {}
        self.summer_no_flow_counts = {}

        for percentile in self.percentilles:
            self.summer_timings[percentile] = []
            self.summer_10_magnitudes[percentile] = []
            self.summer_50_magnitudes[percentile] = []
            self.summer_flush_durations[percentile] = []
            self.summer_wet_durations[percentile] = []
            self.summer_no_flow_counts[percentile] = []

        self.metrics = {'SU_BFL_Tim':{},'SU_BFL_Mag_10':{},'SU_BFL_Mag_50':{},'SU_BFL_Dur_Fl':{},'SU_BFL_Dur_Wet':{},'SU_BFL_No_Flow':{}}
        for key in self.metrics:
            for number in range(1,10):
                self.metrics[key][number] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.start_of_summer()
        current_gauge.fall_flush_timings_durations()
        current_gauge.summer_baseflow_durations_magnitude()

        """Remove offset"""
        for percentile in self.percentilles:
            current_gauge_summer_timing = np.nanpercentile(current_gauge.summer_timings, percentile)
            current_gauge_summer_timing = remove_offset_from_julian_date(current_gauge_summer_timing, self.julian_start_date)

            self.summer_timings[percentile].append(current_gauge_summer_timing)
            self.summer_10_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_10_magnitudes, percentile))
            self.summer_50_magnitudes[percentile].append(np.nanpercentile(current_gauge.summer_50_magnitudes, percentile))
            self.summer_flush_durations[percentile].append(np.nanpercentile(current_gauge.summer_flush_durations, percentile))
            self.summer_wet_durations[percentile].append(np.nanpercentile(current_gauge.summer_wet_durations, percentile))
            self.summer_no_flow_counts[percentile].append(np.nanpercentile(current_gauge.summer_no_flow_counts, percentile))

        """Get nonP result"""
        self.metrics['SU_BFL_Tim'][current_gauge.class_number] += list(current_gauge.summer_timings)
        self.metrics['SU_BFL_Mag_10'][current_gauge.class_number] += list(current_gauge.summer_10_magnitudes)
        self.metrics['SU_BFL_Mag_50'][current_gauge.class_number] += list(current_gauge.summer_50_magnitudes)
        self.metrics['SU_BFL_Dur_Fl'][current_gauge.class_number] += list(current_gauge.summer_flush_durations)
        self.metrics['SU_BFL_Dur_Wet'][current_gauge.class_number] += list(current_gauge.summer_wet_durations)
        self.metrics['SU_BFL_No_Flow'][current_gauge.class_number] += list(current_gauge.summer_no_flow_counts)

    def result_to_csv(self):
        column_header = ['Class', 'Gauge', 'SU_Tim_10','SU_BFL_Mag_10_10','SU_BFL_Mag_50_10','SU_BFL_Dur_Flush_10', 'SU_BFL_Dur_Wet_10', 'SU_BFL_NoFlow_10', 'SU_Tim_50','SU_BFL_Mag_10_50','SU_BFL_Mag_50_50','SU_BFL_Dur_Flush_50', 'SU_BFL_Dur_Wet_50', 'SU_BFL_NoFlow_50','SU_Tim_90','SU_BFL_Mag_10_90','SU_BFL_Mag_50_90','SU_BFL_Dur_Flush_90', 'SU_BFL_Dur_Wet_90', 'SU_BFL_NoFlow_90']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percentile in self.percentilles:
            result_matrix.append(self.summer_timings[percentile])
            result_matrix.append(self.summer_10_magnitudes[percentile])
            result_matrix.append(self.summer_50_magnitudes[percentile])
            result_matrix.append(self.summer_flush_durations[percentile])
            result_matrix.append(self.summer_wet_durations[percentile])
            result_matrix.append(self.summer_no_flow_counts[percentile])

        result_matrix = sort_matrix(result_matrix,0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/summer_baseflow_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
        if self.plot:
            smart_plot(result_matrix)

        """nonP plots"""
        SU_BFL_Tim = []
        SU_BFL_Mag_10 = []
        SU_BFL_Mag_50 = []
        SU_BFL_Dur_Fl = []
        SU_BFL_Dur_Wet = []
        SU_BFL_No_Flow = []

        for class_id in range(1,10):
            SU_BFL_Tim.append(self.metrics['SU_BFL_Tim'][class_id])
            SU_BFL_Mag_10.append(self.metrics['SU_BFL_Mag_10'][class_id])
            SU_BFL_Mag_50.append(self.metrics['SU_BFL_Mag_50'][class_id])
            SU_BFL_Dur_Fl.append(self.metrics['SU_BFL_Dur_Fl'][class_id])
            SU_BFL_Dur_Wet.append(self.metrics['SU_BFL_Dur_Wet'][class_id])
            SU_BFL_No_Flow.append(self.metrics['SU_BFL_No_Flow'][class_id])

        combined = {'SU_BFL_Tim': SU_BFL_Tim, 'SU_BFL_Mag_10': SU_BFL_Mag_10, 'SU_BFL_Mag_50': SU_BFL_Mag_50, 'SU_BFL_Dur_Fl, ': SU_BFL_Dur_Fl, 'SU_BFL_Dur_Wet': SU_BFL_Dur_Wet, 'SU_BFL_No_Flow': SU_BFL_No_Flow}
        if self.plot:
            nonP_box_plot(combined)
