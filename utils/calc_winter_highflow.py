import numpy as np
from utils.helpers import median_of_time
from classes.FlowExceedance import FlowExceedance

def calc_winter_highflow_annual(matrix, exceedance_percent):
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

            # date = get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date)

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    current_flow_object[percent].end_date = row_number

                    exceedance_duration[percent].append(current_flow_object[percent].duration)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        exceedance_object[percent].append(FlowExceedance(row_number, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                    else:
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1

        for percent in exceedance_percent:
            freq[percent].append(len(exceedance_object[percent]))
            duration[percent].append(np.nanmedian(exceedance_duration[percent]))
            timing[percent].append(median_of_time(exceedance_object[percent]))

    return timing, duration, freq

def calc_winter_highflow_POR(matrix, exceedance_percent):

    exceedance_object = {}
    exceedance_value = {}
    current_flow_object = {}
    freq = {}
    duration = {}
    timing = {}
    magnitude = {}
    average_annual_flow = np.nanmedian(matrix)

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

            for percent in exceedance_percent:
                if flow_row < exceedance_value[percent] and current_flow_object[percent] or row_number == len(matrix[:, column_number]) - 1 and current_flow_object[percent]:
                    """End of a object if it falls below threshold, or end of column"""
                    current_flow_object[percent].end_date = row_number + 1
                    duration[percent].append(current_flow_object[percent].duration)
                    magnitude[percent].append(max(current_flow_object[percent].flow) / average_annual_flow)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        """Begining of a object"""
                        exceedance_object[percent].append(FlowExceedance(row_number + 1, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                        timing[percent].append(row_number + 1)
                        freq[percent] = freq[percent] + 1
                    else:
                        """Continue of a object"""
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1


    return timing, duration, freq, magnitude
