import numpy as np
from params import general_params as def_gen_params
from utils.helpers import set_user_params


def calc_all_year(flow_matrix, general_params=def_gen_params):
    key = 'max_nan_allowed_per_year'

    params = set_user_params(general_params, def_gen_params)

    max_nan_allowed_per_year = params[key]

    average_annual_flows = []
    standard_deviations = []
    coefficient_variations = []
    for index, _ in enumerate(flow_matrix[0]):
        average_annual_flows.append(None)
        standard_deviations.append(None)
        coefficient_variations.append(None)

        """Check to see if water year has more than allowed nan or zeros"""
        if np.isnan(flow_matrix[:, index]).sum() > max_nan_allowed_per_year:
            continue

        average_annual_flows[-1] = np.nanmean(flow_matrix[:, index])
        standard_deviations[-1] = np.nanstd(flow_matrix[:, index])
        coefficient_variations[-1] = standard_deviations[-1] / \
            average_annual_flows[-1]

    return average_annual_flows, standard_deviations, coefficient_variations


def calculate_matrix_percentile(matrix):
    ten_percentile_array = []
    fifty_percentile_array = []
    ninty_percentile_array = []

    index = 0
    for flow in matrix[0]:
        ten_percentile_array.append(np.nanpercentile(matrix[:, index], 10))
        fifty_percentile_array.append(np.nanpercentile(matrix[:, index], 50))
        ninty_percentile_array.append(np.nanpercentile(matrix[:, index], 90))
        index = index + 1
    return ten_percentile_array, fifty_percentile_array, ninty_percentile_array


def calculate_average_each_column(matrix):
    average = []

    index = 0
    for flow in matrix[0]:
        average.append(np.nanmean(matrix[:, index]))
        index = index + 1

    return average


def calculate_average_each_row(matrix):
    row_average = []

    for index, flow in enumerate(matrix[:, 0]):
        row_average.append(np.nanmean(matrix[index, :]))

    return row_average


def calculate_std_each_column(matrix):
    std = []

    index = 0
    for flow in matrix[0]:
        std.append(np.nanstd(matrix[:, index]))
        index = index + 1

    return std


def calculate_cov_each_column(std_array, average_array):
    cov = []

    index = 0
    for average in average_array:
        cov.append(std_array[index] / average)
        index = index + 1
    return cov


def calculate_percent_exceedance(matrix):
    two = []
    five = []
    ten = []
    twenty = []
    fifty = []

    index = 0
    for flow in matrix[0]:
        two.append(np.nanpercentile(matrix[:, index], 98))
        five.append(np.nanpercentile(matrix[:, index], 95))
        ten.append(np.nanpercentile(matrix[:, index], 90))
        twenty.append(np.nanpercentile(matrix[:, index], 80))
        fifty.append(np.nanpercentile(matrix[:, index], 50))
        index = index + 1

    return two, five, ten, twenty, fifty
