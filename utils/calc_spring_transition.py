import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from utils.helpers import crossings_nonzero_all, find_index, peakdet

def calc_spring_transition_timing_magnitude(flow_matrix):
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    max_peak_flow_date = 300 # max search date for the peak flow date
    search_window_left = 20
    search_window_right = 50
    peak_sensitivity = 0.5 # smaller => more peaks detection
    peak_filter_percentage = 0.5
    min_max_flow_rate = 2
    window_sigma = 10
    fit_sigma = 1.3 # smaller => less filter
    sensitivity = 0.2 # 0.1 - 10, 0.1 being the most sensitive
    min_percentage_of_max_flow = 0.3 # the detect date's flow has be certain percetage of the max flow
    days_after_peak = 4

    timings = []
    magnitudes = []
    for column_number, column_flow in enumerate(flow_matrix[0]):
        current_sensitivity = sensitivity / 1000

        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year:
            timings.append(None)
            magnitudes.append(None)
            continue;

        """Check to see if it has more than 36 nan"""
        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Using Gaussian with heavy sigma to normalize the curve"""
        filter_data = gaussian_filter1d(flow_data, window_sigma)

        """Find the peaks and valleys of the filtered data"""
        mean_flow = np.nanmean(filter_data)
        maxarray, minarray = peakdet(filter_data, mean_flow * peak_sensitivity)

        """Find the max flow in the curve and determine the window"""
        max_flow_index = find_index(filter_data, np.nanmax(filter_data))

        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date and filter_data[int(flow_index[0])] > np.nanmax(filter_data) * peak_filter_percentage:
                max_flow_index = int(flow_index[0])
                break

        if np.nanmax(filter_data) < min_max_flow_rate:
            """Set spring index to the max flow index, when the annual max flow is below certain threshold.
            This is used when the flow data is stepping
            """
            max_filter_data = np.nanmax(flow_data)
            timings.append(find_index(flow_data, max_filter_data))
            magnitudes.append(max_filter_data)
        else:
            if max_flow_index < search_window_left:
                search_window_left = 0
            if max_flow_index > 366 - search_window_right:
                search_window_right = 366 - max_flow_index

            max_flow_index_window = max(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right])
            timings.append(find_index(flow_data, max_flow_index_window))
            magnitudes.append(max_flow_index_window)

            """Gaussian filter again on the windowed data"""

            x_axis_window = list(range(max_flow_index - search_window_left, max_flow_index + search_window_right))
            flow_data_window = gaussian_filter1d(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right], fit_sigma)

            """Fitting spline on top of the curve"""

            if len(flow_data_window) < 50:
                continue

            spl = ip.UnivariateSpline(x_axis_window, flow_data_window, k=3, s=3)
            spl_first = spl.derivative(1)

            """Derivative of spline where it crosses zero"""
            index_zeros = crossings_nonzero_all(spl_first(x_axis_window))

            """Offset the new index"""
            new_index = []
            for index in index_zeros:
                new_index.append(max_flow_index - search_window_left + index)

            """Loop through the crossing backward"""
            for i in reversed(new_index):
                threshold = max(spl_first(x_axis_window))
                max_flow_window = max(spl(x_axis_window))

                if spl(i) - spl(i-1) > threshold * current_sensitivity * 1 and spl(i-1) - spl(i-2) > threshold * current_sensitivity * 2 and spl(i-2) - spl(i-3) > threshold * current_sensitivity * 3 and spl(i-3) - spl(i-4) > threshold * current_sensitivity * 4 and spl(i) > max_flow_window * min_percentage_of_max_flow:
                    timings[-1] = i;
                    break;

            """Check if timings is before max flow index"""
            if timings[-1] < max_flow_index:
                timings[-1] = max_flow_index + days_after_peak

            """Find max 4 days before and 7 days ahead"""
            if len(flow_data[timings[-1] - 4 : timings[-1] + 7]) > 10:
                max_flow_window_new = max(flow_data[timings[-1] - 4 : timings[-1] + 7])
                new_timings = find_index(flow_data[timings[-1] - 4 : timings[-1] + 7], max_flow_window_new)
                timings[-1] = timings[-1] - 4 + new_timings + days_after_peak
                magnitudes[-1] = max_flow_window_new

            # _spring_transition_plotter(x_axis, flow_data, filter_data, x_axis_window, spl_first, new_index, max_flow_index, timings, search_window_left, search_window_right, spl, column_number)

    return timings, magnitudes

def calc_spring_transition_roc(flow_matrix, spring_timings, summer_timings):
    """Three methods to calculate rate of change
    1. median of daily rate of change
    2. median of daily rate of change only for positive changes
    3. start - end / days
    """
    rocs = []
    rocs_start_end = []
    rocs_only_pos = []

    index = 0
    for spring_timing, summer_timing in zip(spring_timings, summer_timings):
        rate_of_change = []
        rate_of_change_pos = []
        rate_of_change_start_end = None

        if not math.isnan(spring_timing) and not math.isnan(summer_timing):

            if index == len(spring_timings) - 1:
                raw_flow = list(flow_matrix[:,index]) + list(flow_matrix[:30, index])
            else:
                raw_flow = list(flow_matrix[:,index]) + list(flow_matrix[:30, index + 1])

            flow_data = raw_flow[int(spring_timing) : int(summer_timing)]
            rate_of_change_start_end = (flow_data[0] - flow_data[-1]) / len(flow_data)

            for flow_index, data in enumerate(flow_data):
                if flow_index == len(flow_data) - 1:
                    rate_of_change.append(None)
                elif flow_data[flow_index + 1] < flow_data[flow_index]:
                    rate_of_change.append(flow_data[flow_index + 1] - flow_data[flow_index])
                    rate_of_change_pos.append(flow_data[flow_index + 1] - flow_data[flow_index])
                else:
                    rate_of_change.append(None)
                    rate_of_change_pos.append(flow_data[flow_index + 1] - flow_data[flow_index])

        else:
            rocs.append(None)
            rocs_start_end.append(None)
            rocs_only_pos.append(None)
            index = index + 1
            continue

        rate_of_change = np.array(rate_of_change, dtype=np.float)
        rate_of_change_pos = np.array(rate_of_change_pos, dtype=np.float)

        rocs.append(np.nanmedian(rate_of_change))
        rocs_start_end.append(rate_of_change_start_end * -1)
        rocs_only_pos.append(np.nanmedian(rate_of_change_pos))

        index = index + 1

    return rocs_start_end


def _spring_transition_plotter(x_axis, flow_data, filter_data, x_axis_window, spl_first, new_index, max_flow_index, timing, search_window_left, search_window_right, spl, column_number):

    plt.figure()
    plt.plot(x_axis, flow_data, '.')
    plt.plot(x_axis, filter_data)
    plt.plot(x_axis_window, spl_first(x_axis_window))
    plt.plot(new_index, spl_first(new_index), 'x')

    plt.axvline(x = max_flow_index, color='green', ls=':')
    plt.axvline(x = timing[-1], color='red')
    plt.axvline(x = max_flow_index - search_window_left)
    plt.axvline(x = max_flow_index + search_window_right)

    plt.plot(x_axis_window, spl(x_axis_window))
    # plt.yscale('log')
    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
