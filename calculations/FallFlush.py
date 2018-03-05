from datetime import datetime
import numpy as np
from classes.Abstract import Abstract
from utils.helpers import smart_plot, remove_offset_from_julian_date, nonP_box_plot
from utils.matrix_convert import sort_matrix, insert_column_header

class FallFlush(Abstract):

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers, plot):
        Abstract.__init__(self, start_date, directory_name, end_with, class_number, gauge_numbers)
        self.plot = plot
        self._prepare_result_arrays()
        self.julian_start_date = datetime.strptime("{}/2001".format(self.start_date), "%m/%d/%Y").timetuple().tm_yday

    def _prepare_result_arrays(self):
        self.gauge_class_array = []
        self.gauge_number_array = []
        self.fall_timings = {}
        self.fall_magnitudes = {}
        self.fall_durations = {}
        self.fall_wet_timings = {}

        for percent in self.percentilles:
            self.fall_timings[percent] = []
            self.fall_magnitudes[percent] = []
            self.fall_durations[percent] = []
            self.fall_wet_timings[percent] = []

        self.metrics = {'FAFL_Tim':{},'FAFL_Mag':{},'FAFL_Tim_Wet':{},'FAFL_Dur':{}}
        for key in self.metrics:
            for number in range(1,10):
                self.metrics[key][number] = []

    def general_info(self, current_gauge_class, current_gauge_number):
        self.gauge_class_array.append(current_gauge_class)
        self.gauge_number_array.append(current_gauge_number)

    def get_result_arrays(self, current_gauge):
        current_gauge.fall_flush_timings_durations()

        """Remove offset"""
        for percent in self.percentilles:
            current_gauge_fall_timing = np.nanpercentile(current_gauge.fall_timings, percent)
            current_gauge_fall_wet_timing = np.nanpercentile(current_gauge.fall_wet_timings, percent)
            current_gauge_fall_timing = remove_offset_from_julian_date(current_gauge_fall_timing, self.julian_start_date)
            current_gauge_fall_wet_timing = remove_offset_from_julian_date(current_gauge_fall_wet_timing, self.julian_start_date)

            self.fall_timings[percent].append(current_gauge_fall_timing)
            self.fall_magnitudes[percent].append(np.nanpercentile(current_gauge.fall_magnitudes, percent))
            self.fall_wet_timings[percent].append(current_gauge_fall_wet_timing)
            self.fall_durations[percent].append(np.nanpercentile(current_gauge.fall_durations, percent))

        """Get nonP result"""
        self.metrics['FAFL_Tim'][current_gauge.class_number] += list(current_gauge.fall_timings)
        self.metrics['FAFL_Mag'][current_gauge.class_number] += list(current_gauge.fall_magnitudes)
        self.metrics['FAFL_Tim_Wet'][current_gauge.class_number] += list(current_gauge.fall_wet_timings)
        self.metrics['FAFL_Dur'][current_gauge.class_number] += list(current_gauge.fall_durations)

    def result_to_csv(self):
        column_header = ['Class', 'Gauge', 'FAFL_Tim_10%', 'FAFL_Mag_10%', 'FAFL_Dur_10%', 'FA_Tim_Wet_10%', 'FAFL_Tim_50%', 'FAFL_Mag_50%', 'FAFL_Dur_50%', 'FA_Tim_Wet_50%', 'FAFL_Tim_90%', 'FAFL_Mag_90%', 'FAFL_Dur_90%', 'FA_Tim_Wet_90%']
        result_matrix = []
        result_matrix.append(self.gauge_class_array)
        result_matrix.append(self.gauge_number_array)

        for percent in self.percentilles:
            result_matrix.append(self.fall_timings[percent])
            result_matrix.append(self.fall_magnitudes[percent])
            result_matrix.append(self.fall_durations[percent])
            result_matrix.append(self.fall_wet_timings[percent])

        result_matrix = sort_matrix(result_matrix, 0)
        result_matrix = insert_column_header(result_matrix, column_header)

        np.savetxt("post_processedFiles/fall_flush_result_matrix.csv", result_matrix, delimiter=",", fmt="%s")
        if self.plot:
            smart_plot(result_matrix)

        """nonP plots"""
        FAFL_Tim = []
        FAFL_Mag = []
        FAFL_Tim_Wet = []
        FAFL_Dur = []

        for class_id in range(1,10):
            FAFL_Tim.append(self.metrics['FAFL_Tim'][class_id])
            FAFL_Mag.append(self.metrics['FAFL_Mag'][class_id])
            FAFL_Tim_Wet.append(self.metrics['FAFL_Tim_Wet'][class_id])
            FAFL_Dur.append(self.metrics['FAFL_Dur'][class_id])

        combined = {'FAFL_Tim': FAFL_Tim, 'FAFL_Mag': FAFL_Mag, 'FAFL_Tim_Wet': FAFL_Tim_Wet, 'FAFL_Dur': FAFL_Dur}
        if self.plot:
            nonP_box_plot(combined)
