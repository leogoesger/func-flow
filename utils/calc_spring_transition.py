import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
import numpy as np
from utils.helpers import crossings_nonzero_all, find_index

def calc_spring_transition_timing(flow_matrix):
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    search_window_left = 20
    min_max_flow_rate = 1
    window_sigma = 10
    fit_sigma = 1.2 # smaller => less filter
    sensitivity = 7 # 1 - 10, 1 being the most sensitive

    timing = []
    for column_number, column_flow in enumerate(flow_matrix[0]):
        search_window_right_from_end = 100

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

        """Find the max flow in the curve and determine the window"""
        max_flow_index = find_index(filter_data, max(filter_data))

        if max(filter_data) < min_max_flow_rate:
            """Set spring index to the max flow index, when the annual max flow is below certain threshold.
            This is used when the flow data is stepping
            """
            timing.append(find_index(flow_data, max(flow_data)))
        else:
            if max_flow_index < search_window_left:
                search_window_left = 0
            if max_flow_index > 366 - search_window_right_from_end:
                search_window_right_from_end = 5

            print(search_window_right_from_end)
            timing.append(find_index(flow_data, max(flow_data[max_flow_index - search_window_left : len(flow_data) - 20])))

            """Gaussian filter again on the windowed data"""
            x_axis_window = list(range(max_flow_index - search_window_left, len(flow_data) - search_window_right_from_end))
            flow_data_window = gaussian_filter1d(flow_data[max_flow_index - search_window_left : len(flow_data) - search_window_right_from_end], fit_sigma)

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

                sensitivity = sensitivity / 1000
                if spl(i) - spl(i-1) > threshold * sensitivity * 1 and spl(i-1) - spl(i-2) > threshold * sensitivity * 2 and spl(i-2) - spl(i-3) > threshold * sensitivity * 3 and spl(i-3) - spl(i-4) > threshold * sensitivity * 4:
                    timing[-1] = i;
                    break;

            plt.figure()
            plt.plot(x_axis, flow_data, '.')
            plt.plot(x_axis, filter_data)
            plt.axvline(x = timing[-1], color='red')
            plt.axvline(x = len(flow_data) - search_window_right_from_end)
            plt.plot(x_axis_window, spl(x_axis_window))
            plt.yscale('log')
            plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
