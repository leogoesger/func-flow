import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import moving_average, get_nan_fraction_in_array
from utils.helpers import find_index
from scipy.ndimage import gaussian_filter1d


def calc_start_of_summer(matrix):

    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    filter_sigma = 7

    start_dates = []
    failed_calcs = 0

    for index, flow in enumerate(matrix[0]):
        """Check if data has too many zeros or NaN, and if so skip to next water year"""
        if np.isnan(matrix[:, index]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, index]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            continue;


        """Calculate the percentile which gives the 73 lowest flow days in the second half of the water year"""
        matrix_slice = matrix[182 : len(matrix[:, 0]) - 1, index]
        percentile = np.nanpercentile(matrix_slice, 40)

        """Smooth out the timeseries and set search range after smoothed out max flow"""
        smooth_data = gaussian_filter1d(matrix[:,index], filter_sigma)
        search_range = find_index(smooth_data, max(smooth_data))
        if not search_range:
            start_dates.append(None)
            continue;

        for data_index, data in enumerate(smooth_data):

            """For a low flow percentile = 0, only require smoothed flow to stay at Q=0 for three days"""
            if percentile == 0:

                if (data_index > len(smooth_data) - 3):
                    start_dates.append(float('NaN'))
                    break
                elif data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile:
                    start_dates.append(data_index)
            else:
                """When the low flow percentile is above zero, require smoothed flow to stay under threshold for four days"""
                if (data_index > len(smooth_data) - 4):
                    start_dates.append(float('NaN'))
                    break
                if data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile and smooth_data[data_index + 3] <= percentile:
                    start_dates.append(data_index)
                    break

        """Consider test failed if start data is calculated right on the search range or as zero"""
        if start_dates[index] == search_range:
            start_dates[index] == np.nan
        elif start_dates[index] == 0:
            start_dates[index] == np.nan
        elif np.isnan(start_dates[index]) == True:
            failed_calcs = failed_calcs + 1

        # _summer_baseflow_plot(index, smooth_data, start_dates, percentile, search_range)


    # print('Test failed for {} out of {} water years.'.format(failed_calcs, matrix.shape[1]))

    return start_dates

def _summer_baseflow_plot(index, smooth_data, start_dates, percentile, search_range):

    plt.figure(index)
    plt.plot(matrix[:, index], '-')
    plt.plot(smooth_data)
    plt.title('Start of Summer Metric')
    plt.xlabel('Julian Day')
    plt.ylabel('Flow, ft^3/s')
    plt.axvline(start_dates[index], color='red')
    plt.axhline(percentile)
    plt.axvline(search_range, color='green')
    plt.text(0, 0, percentile)
    plt.savefig('post_processedFiles/Summer_baseflow/{}.png'.format(index+1))
