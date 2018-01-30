import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
import numpy as np
from utils.helpers import crossings_nonzero_all, find_index
from collections import OrderedDict

search_window_left = 20
search_window_right_from_end = 50
min_max_flow_rate = 1
window_sigma = 10
fit_sigma = 2
sensitivity = 5 # 1 - 10, 1 being the most sensitive


def calc_spring_transition_timing(flow_matrix):
    for column_number, column_flow in enumerate(flow_matrix[0]):
        if np.isnan(flow_matrix[:, column_number]).sum() < 36:
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
                spring = find_index(flow_data, max(flow_data))
                spring2 = find_index(flow_data, max(flow_data))
            else:
                spring = find_index(flow_data, max(flow_data[max_flow_index - search_window_left : len(flow_data) - 20]))
                spring2 = find_index(flow_data, max(flow_data[max_flow_index - search_window_left : len(flow_data) - 20]))

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
                        spring2 = i;
                        break;

                # for i in reversed(new_index):
                #     array = []
                #     for index in range(7):
                #         array.append(flow_matrix[i - index, column_number])
                #     array = list(OrderedDict.fromkeys(array))
                #     print(i, array)
                #     if len(array) < 5:
                #         continue
                #     elif array[0] > array[1] and array[1] > array[2] and array[2] > array[3] and array[3] > array[4]:
                #         spring = i
                #         break

                # plt.figure()
                # plt.plot(x_axis, filter_data, '.')
                # plt.plot(x_axis, flow_data, '.')
                # plt.plot(max_flow_index, flow_data[max_flow_index], 'v')
                #
                # plt.axvline(x = max_flow_index - search_window_left)
                # plt.axvline(x = len(flow_data) - search_window_right_from_end)
                #
                # plt.plot(x_axis_window, spl(x_axis_window), color='green')
                # plt.plot(x_axis_window, spl_first(x_axis_window), color='purple')
                # plt.plot(new_index, spl_first(new_index), 'x')
                #
                # print(spring, spring2)
                # plt.plot(spring, flow_data[spring], 'v', c='blue')
                # plt.plot(spring2, flow_data[spring2], '^', c='red')
                #
                # plt.savefig('post_processedFiles/Boxplots/{}.png'.format(number))
