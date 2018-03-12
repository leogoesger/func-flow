import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from utils.helpers import crossings_nonzero_all, find_index, peakdet, replace_nan
from params import spring_params

def calc_spring_transition_timing_magnitude(flow_matrix):
    max_zero_allowed_per_year = spring_params['max_zero_allowed_per_year']
    max_nan_allowed_per_year = spring_params['max_nan_allowed_per_year']
    max_peak_flow_date = spring_params['max_peak_flow_date'] # max search date for the peak flow date
    search_window_left = spring_params['search_window_left'] # left side of search window set around max peak
    search_window_right = spring_params['search_window_right'] # right side of search window set around max peak
    peak_sensitivity = spring_params['peak_sensitivity'] # smaller => more peaks detection
    peak_filter_percentage = spring_params['peak_filter_percentage'] # Relative flow (Q-Qmin) of start of spring must be certain percentage of peak relative flow (Qmax-Qmin)
    min_max_flow_rate = spring_params['min_max_flow_rate']
    window_sigma = spring_params['window_sigma'] # Heavy filter to identify major peaks in entire water year
    fit_sigma = spring_params['fit_sigma'] # Smaller filter to identify small peaks in windowed data (smaller sigma val => less filter)
    sensitivity = spring_params['sensitivity'] # 0.1 - 10, 0.1 being the most sensitive
    min_percentage_of_max_flow = spring_params['min_percentage_of_max_flow'] # the detected date's flow has be certain percetage of the max flow in that region
    lag_time = spring_params['lag_time']

    timings = []
    magnitudes = []
    for column_number, column_flow in enumerate(flow_matrix[0]):
        current_sensitivity = sensitivity / 1000

        timings.append(None)
        magnitudes.append(None)

        """Check to see if water year has more than allowed nan or zeros"""
        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year:
            continue

        """Get flow data and interpolate between None values"""
        flow_data = flow_matrix[:, column_number]
        flow_data = replace_nan(flow_data)
        x_axis = list(range(len(flow_data))) # Extract for use in optional plotting

        """Using Gaussian with heavy sigma to smooth the curve"""
        filter_data = gaussian_filter1d(flow_data, window_sigma)

        """Find the peaks and valleys of the filtered data"""
        mean_flow = np.nanmean(filter_data)
        maxarray, minarray = peakdet(filter_data, mean_flow * peak_sensitivity) # Returns array with the index and flow magnitude for each peak and valley

        """Find the max flow in the curve and determine flow range requirements"""
        max_flow = np.nanmax(filter_data)
        max_flow_index = find_index(filter_data, max_flow)
        min_flow = np.nanmin(filter_data)
        flow_range = max_flow - min_flow

        """Identify rightmost peak that fulfills date and magnitude requirements"""
        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date and (flow_index[1] - min_flow) / flow_range > peak_filter_percentage:
                max_flow_index = int(flow_index[0])
                break

        if np.nanmax(filter_data) < min_max_flow_rate:
            """Set start of spring index to the max flow index, when the annual max flow is below certain threshold.
            This is used for extremely low flows where data appears to be stepwise
            """
            max_filter_data = np.nanmax(flow_data)
            timings[-1] = find_index(flow_data, max_filter_data)
            magnitudes[-1] = max_filter_data
        else:
            if max_flow_index < search_window_left:
                search_window_left = 0
            if max_flow_index > 366 - search_window_right:
                search_window_right = 366 - max_flow_index

            """Get indices of windowed data"""
            max_flow_index_window = max(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right])
            timings[-1] = find_index(flow_data, max_flow_index_window)
            magnitudes[-1] = max_flow_index_window

            """Gaussian filter again on the windowed data (smaller filter this time)"""
            x_axis_window = list(range(max_flow_index - search_window_left, max_flow_index + search_window_right))
            flow_data_window = gaussian_filter1d(flow_data[max_flow_index - search_window_left : max_flow_index + search_window_right], fit_sigma)

            """Fit a spline on top of the Gaussian curve"""
            if len(flow_data_window) < 50:
                continue

            spl = ip.UnivariateSpline(x_axis_window, flow_data_window, k=3, s=3)

            """Calculate the first derivative of the spline"""
            spl_first_deriv = spl.derivative(1)

            """Find where the derivative of the spline crosses zero"""
            index_zeros = crossings_nonzero_all(spl_first_deriv(x_axis_window))

            """Offset the new index"""
            new_index = []
            for index in index_zeros:
                new_index.append(max_flow_index - search_window_left + index)

            """Loop through the indices where derivative=0, from right to left"""
            for i in reversed(new_index):
                threshold = max(spl_first_deriv(x_axis_window))
                max_flow_window = max(spl(x_axis_window))
                min_flow_window = min(spl(x_axis_window))
                range_window = max_flow_window - min_flow_window

                """Set spring timing as index which fulfills the following requirements"""
                if spl(i) - spl(i-1) > threshold * current_sensitivity * 1 and spl(i-1) - spl(i-2) > threshold * current_sensitivity * 2 and spl(i-2) - spl(i-3) > threshold * current_sensitivity * 3 and spl(i-3) - spl(i-4) > threshold * current_sensitivity * 4 and (spl(i) - min_flow_window) / range_window > min_percentage_of_max_flow:
                    timings[-1] = i;
                    break;

            """Check if timings is before max flow index"""
            if timings[-1] < max_flow_index:
                timings[-1] = max_flow_index + lag_time

            """Find max flow 4 days before and 7 days ahead. Assign as new start date"""
            if len(flow_data[timings[-1] - 4 : timings[-1] + 7]) > 10:
                max_flow_window_new = max(flow_data[timings[-1] - 4 : timings[-1] + 7])
                new_timings = find_index(flow_data[timings[-1] - 4 : timings[-1] + 7], max_flow_window_new)
                timings[-1] = timings[-1] - 4 + new_timings + lag_time
                magnitudes[-1] = max_flow_window_new

            # _spring_transition_plotter(x_axis, flow_data, filter_data, x_axis_window, spl_first_deriv, new_index, max_flow_index, timings, search_window_left, search_window_right, spl, column_number, maxarray)

    return timings, magnitudes

def calc_spring_transition_duration(spring_timings, summer_timings):
    duration_array = []
    for index, spring_timing in enumerate(spring_timings):
        if spring_timing and summer_timings[index] and summer_timings[index] > spring_timing:
            duration_array.append(summer_timings[index] - spring_timing)
        else:
            duration_array.append(None)
    return duration_array

def calc_spring_transition_roc(flow_matrix, spring_timings, summer_timings):
    """Three methods to calculate rate of change
    1. median of daily rate of change
    2. median of daily rate of change only for negative changes
    3. start - end / days
    """
    rocs = []
    rocs_start_end = []
    rocs_only_neg = []

    index = 0
    for spring_timing, summer_timing in zip(spring_timings, summer_timings):
        rate_of_change = []
        rate_of_change_neg = []
        rate_of_change_start_end = None

        if not math.isnan(spring_timing) and not math.isnan(summer_timing) and summer_timing > spring_timing:

            if index == len(spring_timings) - 1:
                raw_flow = list(flow_matrix[:,index]) + list(flow_matrix[:30, index])
            else:
                raw_flow = list(flow_matrix[:,index]) + list(flow_matrix[:30, index + 1])

            flow_data = raw_flow[int(spring_timing) : int(summer_timing)]
            rate_of_change_start_end = (flow_data[-1] - flow_data[0]) / flow_data[0]

            for flow_index, data in enumerate(flow_data):
                if flow_index == len(flow_data) - 1:
                    continue
                elif flow_data[flow_index + 1] < flow_data[flow_index]:
                    rate_of_change.append(( flow_data[flow_index] - flow_data[flow_index + 1] ) / flow_data[flow_index])
                    rate_of_change_neg.append((flow_data[flow_index] - flow_data[flow_index + 1]) / flow_data[flow_index])
                else:
                    rate_of_change.append((flow_data[flow_index] - flow_data[flow_index + 1]) / flow_data[flow_index])

        else:
            rocs.append(None)
            rocs_start_end.append(None)
            rocs_only_neg.append(None)
            index = index + 1
            continue

        rate_of_change = np.array(rate_of_change, dtype=np.float)
        rate_of_change_neg = np.array(rate_of_change_neg, dtype=np.float)

        rocs.append(np.nanmedian(rate_of_change))
        rocs_start_end.append(rate_of_change_start_end)
        rocs_only_neg.append(np.nanmedian(rate_of_change_neg))

        index = index + 1
    return rocs_only_neg


def _spring_transition_plotter(x_axis, flow_data, filter_data, x_axis_window, spl_first_deriv, new_index, max_flow_index, timing, search_window_left, search_window_right, spl, column_number, maxarray):

    plt.figure()
    plt.plot(x_axis, flow_data)
    plt.plot(x_axis, filter_data)
    plt.plot(x_axis_window, spl_first_deriv(x_axis_window))
    plt.plot(new_index, spl_first_deriv(new_index), 'x')

    plt.axvline(x = max_flow_index, color='green', ls=':')
    plt.axvline(x = timing[-1], color='red')
    plt.axvline(x = max_flow_index - search_window_left)
    plt.axvline(x = max_flow_index + search_window_right)

    for data in maxarray:
        plt.plot(data[0], data[1], '^')

    plt.plot(x_axis_window, spl(x_axis_window))
    # plt.yscale('log')
    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
