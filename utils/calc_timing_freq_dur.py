import numpy as np
from helpers import get_date_from_offset_julian_date


def median_of_time(lt):
    n = len(lt)
    if n < 1:
        return None
    elif n % 2 ==  1:
        return lt[n//2].start_date.timetuple().tm_yday
    elif n == 2:
        first_date = lt[0].start_date.timetuple().tm_yday
        second_date = lt[1].start_date.timetuple().tm_yday
        return (first_date + second_date) / 2
    else:
        first_date = lt[n//2 - 1].start_date.timetuple().tm_yday
        second_date = lt[n//2 + 1].start_date.timetuple().tm_yday
        return (first_date + second_date) / 2


class flowExceedance:

    def __init__(self, start_date, end_date, duration, exceedance):
        self.start_date = start_date
        self.end_date = end_date
        self.duration = duration
        self.flow = []
        self.exceedance = exceedance

    def add_flow(self, flow_data):
        self.flow.append(flow_data)



def calculate_timing_duration_frequency(matrix, year_ranges, start_date, exceedance_percent):

    exceedance_value = {}
    freq = {}
    duration = {}
    timing = {}

    for i in exceedance_percent:
        exceedance_value[i] = np.nanpercentile(matrix, 100 - i)
        freq[i] = []
        duration[i] = []
        timing[i] = []

    for column_number, flow_column in enumerate(matrix[0]):

        exceedance_object = {}
        exceedance_duration = {}
        current_flow_object = {}

        """Init current flow object"""
        for i in exceedance_percent:
            exceedance_object[i] = []
            exceedance_duration[i] = []
            current_flow_object[i] = None

        for row_number, flow_row in enumerate(matrix[:, column_number]):

            current_date = get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date)

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    current_flow_object[percent].end_date = current_date

                    exceedance_duration[percent].append(current_flow_object[percent].duration)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        exceedance_object[percent].append(flowExceedance(current_date, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                    else:
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1

        for i in exceedance_percent:
            freq[i].append(len(exceedance_object[i]))
            duration[i].append(np.nanmedian(exceedance_duration[i]))
            timing[i].append(median_of_time(exceedance_object[i]))

    return timing, duration, freq
