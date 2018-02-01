import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks_cwt
import numpy as np
from utils.helpers import crossings_nonzero_all, find_index, peakdet

def calc_spring_transition_timing(flow_matrix):
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    max_peak_flow_date = 300 # max search date for the peak flow date
    search_window_left = 20
    search_window_right = 50
    peak_sensitivity = 0.2 # smaller => more peaks detection
    min_max_flow_rate = 2
    window_sigma = 10
    fit_sigma = 1.2 # smaller => less filter
    sensitivity = 0.2 # 0.1 - 10, 0.1 being the most sensitive

    timing = []
    for column_number, column_flow in enumerate(flow_matrix[0]):
        current_sensitivity = sensitivity / 1000

        print('$$$$$$$$$$$$$$$$')
        print(column_number)
        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year:
            timing.append(None)
            continue;

        """Check to see if it has more than 36 nan"""
        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Using Gaussian with heavy sigma to normalize the curve"""
        filter_data = gaussian_filter1d(flow_data, window_sigma)

        """Find the peaks and valleys of the filtered data"""
        median_flow = np.nanmean(flow_data)
        maxarray, minarray = peakdet(filter_data, median_flow * peak_sensitivity)

        """Find the max flow in the curve and determine the window"""
        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date:
                max_flow_index = int(flow_index[0])
                break

        if max(filter_data) < min_max_flow_rate:
            """Set spring index to the max flow index, when the annual max flow is below certain threshold.
            This is used when the flow data is stepping
            """
            timing.append(find_index(flow_data, max(flow_data)))
        else:
            if max_flow_index < search_window_left:
                search_window_left = 0
            if max_flow_index > 366 - search_window_right:
                search_window_right = 366 - max_flow_index


            timing.append(find_index(flow_data, max(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right])))

            """Gaussian filter again on the windowed data"""

            x_axis_window = list(range(max_flow_index - search_window_left, max_flow_index + search_window_right))
            flow_data_window = gaussian_filter1d(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right], fit_sigma)

            """Fitting spline on top of the curve"""

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

                if spl(i) - spl(i-1) > threshold * current_sensitivity * 1 and spl(i-1) - spl(i-2) > threshold * current_sensitivity * 2 and spl(i-2) - spl(i-3) > threshold * current_sensitivity * 3 and spl(i-3) - spl(i-4) > threshold * current_sensitivity * 4:
                    timing[-1] = i;
                    break;

            """Check if timing is before max flow index"""
            if timing[-1] < max_flow_index:
                timing[-1] = max_flow_index

            _spring_transition_plotter(x_axis, flow_data, filter_data, x_axis_window, spl_first, new_index, max_flow_index, timing, search_window_left, search_window_right, spl, column_number)

    print(timing)
    return timing

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
