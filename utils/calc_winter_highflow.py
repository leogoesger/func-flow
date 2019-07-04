import numpy as np
from utils.helpers import median_of_time, median_of_magnitude, peak_magnitude, set_user_params
from classes.FlowExceedance import FlowExceedance
from params import winter_params as def_winter_params

def calc_winter_highflow_annual(matrix, exceedance_percent, winter_params = def_winter_params):

    params = set_user_params(winter_params, def_winter_params)

    max_nan_allowed_per_year, max_zero_allowed_per_year = params.values()

    """Get peak percentiles calculated from each year's peak flow values"""
    peak_flows = []
    percentiles = [2,5,10,20]
    peak_exceedance_values = []
    for column_number, _ in enumerate(matrix[0]):
        flow_data = matrix[:, column_number]
        peak_flows.append(np.nanmax(flow_data))
    for percentile in percentiles:
        peak_exceedance_values.append(np.nanpercentile(peak_flows, 100 - percentile))

    """Add high flow percentiles and peak flow percentile together for final list of exceedance values"""
    highflow_exceedance_values = []
    for i in exceedance_percent:
        highflow_exceedance_values.append(np.nanpercentile(matrix, 100 - i))
    exceedance_values = peak_exceedance_values + highflow_exceedance_values # four peak exceedance vals plus five high flow exceedance vals, only first eight get reported. 

    exceedance_value = {}
    freq = {}
    duration = {}
    timing = {}
    magnitude = {}
    peak_magnitude = {}

    for i, value in enumerate(exceedance_values):
        exceedance_value[i] = value
        freq[i] = []
        duration[i] = []
        timing[i] = []
        magnitude[i] = []
        peak_magnitude[i] = []

    for column_number, flow_column in enumerate(matrix[0]):

        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number] == 0) > max_zero_allowed_per_year:
            for i, value in enumerate(exceedance_values):
                freq[i].append(None)
                duration[i].append(None)
                timing[i].append(None)
                magnitude[i].append(None)
                peak_magnitude[i].append(None)
            continue

        exceedance_object = {}
        exceedance_duration = {}
        current_flow_object = {}
        peak_flow = {}

        """Init current flow object"""
        for i, value in enumerate(exceedance_values):
            exceedance_object[i] = []
            exceedance_duration[i] = []
            current_flow_object[i] = None
            peak_flow[i] = []

        """Loop through each flow value for the year to check if they pass exceedance threshold"""
        for row_number, flow_row in enumerate(matrix[:, column_number]):

            for i, value in enumerate(exceedance_values):
                if bool(flow_row < exceedance_value[i] and current_flow_object[i]) or bool(row_number == len(matrix[:, column_number]) - 1 and current_flow_object[i]):
                    """End of an object if it falls below threshold, or end of column"""
                    current_flow_object[i].end_date = row_number + 1
                    current_flow_object[i].get_max_magnitude()
                    exceedance_duration[i].append(current_flow_object[i].duration)
                    peak_flow[i] = np.nanmax(flow_row)
                    current_flow_object[i] = None

                elif flow_row >= exceedance_value[i]:
                    if not current_flow_object[i]:
                        """Beginning of an object"""
                        exceedance_object[i].append(
                            FlowExceedance(row_number, None, 1, i))
                        current_flow_object[i] = exceedance_object[i][-1]
                        current_flow_object[i].add_flow(flow_row)
                    else:
                        """Continuing an object"""
                        current_flow_object[i].add_flow(flow_row)
                        current_flow_object[i].duration = current_flow_object[i].duration + 1
        for i, value in enumerate(exceedance_values):
            freq[i].append(len(exceedance_object[i]))
            duration[i].append(
                np.nansum(exceedance_duration[i]) if not np.isnan(np.nansum(exceedance_duration[i])) else None)
            timing[i].append(median_of_time(exceedance_object[i]))
            magnitude[i].append(exceedance_value[i])
   
    return timing, duration, freq, magnitude


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
                    duration[percent].append(
                        current_flow_object[percent].duration)
                    magnitude[percent].append(
                        max(current_flow_object[percent].flow) / average_annual_flow)
                    current_flow_object[percent] = None

                elif flow_row >= exceedance_value[percent]:
                    if not current_flow_object[percent]:
                        """Begining of a object"""
                        exceedance_object[percent].append(
                            FlowExceedance(row_number + 1, None, 1, percent))
                        current_flow_object[percent] = exceedance_object[percent][-1]
                        current_flow_object[percent].add_flow(flow_row)
                        timing[percent].append(row_number + 1)
                        freq[percent] = freq[percent] + 1
                    else:
                        """Continue of a object"""
                        current_flow_object[percent].add_flow(flow_row)
                        current_flow_object[percent].duration = current_flow_object[percent].duration + 1

    return timing, duration, freq, magnitude
