import numpy as np
from utils.helpers import *

percentiles = [10, 25, 50, 75, 90]
percentile_keys = ["ten", "twenty_five", "fifty", "seventy_five", "ninty"]


def calc_drh(flow_matrix):
    """Dimensionless Hydrograph Plotter"""
    average_annual_flow = calculate_average_each_column(flow_matrix)
    number_of_rows = len(flow_matrix)
    number_of_columns = len(flow_matrix[0, :])
    normalized_matrix = np.zeros((number_of_rows, number_of_columns))

    """Initiating the DRH object with desired keys"""
    drh = {}
    for index, percentile in enumerate(percentiles):
        drh[percentile_keys[index]] = []
    drh["min"] = []
    drh["max"] = []

    for row_index, _ in enumerate(flow_matrix[:, 0]):
        for column_index, _ in enumerate(flow_matrix[row_index, :]):
            normalized_matrix[row_index, column_index] = flow_matrix[row_index,
                                                                     column_index]/average_annual_flow[column_index]
        for index, percentile in enumerate(percentiles):
            drh[percentile_keys[index]].append(round(np.nanpercentile(
                normalized_matrix[row_index, :], percentile), 2))

        drh["min"].append(round(np.nanmin(normalized_matrix[row_index, :]), 2))
        drh["max"].append(round(np.nanmax(normalized_matrix[row_index, :]), 2))

    return drh
