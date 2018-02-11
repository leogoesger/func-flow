import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from utils.helpers import find_index, peakdet, replace_nan

def calc_fall_flush_durations(flow_data, wet_filter_data, date):

    duration_left = None
    duration_right = None
    duration = None

    if date:
        date = int(date)
        for index_left, flow_left in enumerate(reversed(flow_data[:date])):
            if flow_left < wet_filter_data[date - index_left]:
                duration_left = index_left
                break
        for index_right, flow_right in enumerate(flow_data[date:]):
            if flow_right < wet_filter_data[date + index_right]:
                duration_right = index_right
                break

        if duration_left and duration_right:
            duration = duration_left + duration_right
        else:
            duration = None

    return duration

def calc_fall_flush_durations_2(filter_data, date):

    max_perct = 0.05
    duration = None
    left = 0
    right = 0

    if date:
        left_maxarray, left_minarray = peakdet(filter_data[:date + 2], 0.01)
        right_maxarray, right_minarray = peakdet(filter_data[date - 2:], 0.01)

        if not list(left_minarray):
            left = 0
        else:
            left = left_minarray[-1][0]

        if not list(right_minarray):
            right = 0
        else:
            right = date - 2 + right_minarray[0][0]

        max_data = filter_data[date]
        left_min = min(filter_data[left : date])
        right_min = min(filter_data[date : right])

        left_threshold = (max_data - left_min) * max_perct
        right_threhold = (max_data - right_min) * max_perct

        duration = int(right - left)

    return duration, left, right


def calc_fall_flush_timings(flow_matrix):
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    sigma = 1.1
    wet_sigma = 17
    peak_sensitivity = 0.1 # flush hump peak sensitive
    min_flush_duration = 20
    wet_threshold_perc = 0.1
    flush_threshold_perc = 0.30

    start_dates = []
    wet_dates = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            wet_dates.append(None)
            continue;

        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Interplate off None values"""
        flow_data = replace_nan(flow_data)

        """Filter noise data with small sigma to find flush hump"""
        filter_data = gaussian_filter1d(flow_data, sigma)
        wet_filter_data = gaussian_filter1d(flow_data, wet_sigma)

        """Fit spline"""
        x_axis = list(range(len(filter_data)))
        spl = ip.UnivariateSpline(x_axis, filter_data, k=3, s=3)

        """Find the peaks and valleys of the filtered data"""
        mean_flow = np.nanmean(filter_data)
        maxarray, minarray = peakdet(spl(x_axis), mean_flow * peak_sensitivity)

        max_flow = max(filter_data[100:])
        max_flow_index = find_index(filter_data, max_flow)
        min_flow = min(filter_data[:max_flow_index])

        """Get fall flush peak"""
        counter = 0
        half_duration = int(min_flush_duration/2)
        for flow_index in maxarray:
            if counter == 0:
                if flow_index[0] < half_duration and flow_index[0] != 0:
                    """if index found is before the half duration allowed"""
                    start_dates.append(int(flow_index[0]))
                    break
                elif bool((flow_index[1] - spl(maxarray[counter][0] - half_duration)) / flow_index[1] > flush_threshold_perc or minarray[counter][0] - maxarray[counter][0] < half_duration):
                    """If peak and valley is separted by half duration, or half duration to the left is less than 30% of its value"""
                    start_dates.append(int(flow_index[0]))
                    break
            elif minarray[counter][0] - maxarray[counter][0] < half_duration or maxarray[counter][0] - minarray[counter-1][0] < half_duration or bool((flow_index[1] - spl(maxarray[counter][0] - half_duration)) / flow_index[1] > flush_threshold_perc and (flow_index[1] - spl(maxarray[counter][0] + half_duration)) / flow_index[1] > flush_threshold_perc):
                """valley and peak less than half dur from either side or both side of the peak end fall below flush_threshold_perc"""
                start_dates.append(int(flow_index[0]))
                break
            counter = counter + 1

        """Return to Wet Seaon"""
        max_wet_peak_mag = max(wet_filter_data[100:])
        max_wet_peak_index = find_index(wet_filter_data, max_wet_peak_mag)
        min_wet_peak_mag = min(wet_filter_data[:max_wet_peak_index])

        for index, value in enumerate(reversed(wet_filter_data[:max_wet_peak_index])):
            if value / (max_wet_peak_mag - min_wet_peak_mag) < wet_threshold_perc:
                """If value percentage falls below wet_threshold_perc"""
                wet_dates.append(max_wet_peak_index - index)
                max_allowed_date = max_wet_peak_index - index
                break;

        """Check to see if last start_date falls behind the max_allowed_date"""
        if start_dates[-1] > max_allowed_date:
            start_dates[-1] = None

        """Get duration of each fall flush"""
        current_duration = calc_fall_flush_durations(filter_data, wet_filter_data, start_dates[-1])

        current_duration_2, left, right = calc_fall_flush_durations_2(filter_data, start_dates[-1])

        print(column_number, start_dates[-1], current_duration, current_duration_2)
        _plotter(x_axis, flow_data, filter_data, wet_filter_data, start_dates, wet_dates, column_number, left, right)

    return start_dates, wet_dates

def _plotter(x_axis, flow_data, filter_data, wet_filter_data, start_dates, wet_dates, column_number, left, right):
    plt.figure()
    plt.plot(x_axis, flow_data, '.')
    plt.plot(x_axis, filter_data)
    plt.plot(x_axis, wet_filter_data)
    if start_dates[-1] is not None:
        plt.axvline(start_dates[-1], color='blue')
    plt.axvline(wet_dates[-1], color="orange")
    plt.axvline(left, ls=":")
    plt.axvline(right, ls=":")
    plt.yscale('log')
    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
