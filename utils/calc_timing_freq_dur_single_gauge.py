import numpy as np
from utils.helpers import get_date_from_offset_julian_date


class FlowExceedance:

    def __init__(self, start_date, end_date, duration, exceedance):
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.flow = []
        self.exceedance = exceedance

    def add_flow(self, flow_data):
        self.flow.append(flow_data)


def calculate_timing_duration_frequency_single_gauge(matrix, year_ranges, start_date, exceedance_percent):

    exceedance_object = {}
    exceedance_value = {}
    current_flow_object = {}
    freq = {}
    duration = {}
    timing = {}
    magnitude = {}

    for i in exceedance_percent:
        exceedance_value[i] = np.nanpercentile(matrix, 100 - i)
        exceedance_object[i] = []
        current_flow_object[i] = None
        freq[i] = 0
        duration[i] = []
        timing[i] = []
        magnitude[i] = []

    for column_number, flow_column in enumerate(matrix[0]):
        for row_number, flow_row in enumerate(matrix[:, column_number]):

            current_date = get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date)

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    """End of a object if it falls below threshold, or end of column"""
                    current_flow_object[percent].end_date = current_date
                    duration[percent].append(current_flow_object[percent].duration)
                    magnitude[percent].append(max(current_flow_object[percent].flow))
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        """Begining of a object"""
                        exceedance_object[percent].append(FlowExceedance(current_date, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                        timing[percent].append(current_date.timetuple().tm_yday)
                        freq[percent] = freq[percent] + 1
                    else:
                        """Continue of a object"""
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1


    return timing, duration, freq, magnitude
