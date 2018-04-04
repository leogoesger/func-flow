import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from utils.helpers import find_index, peakdet, replace_nan
from params import fall_params

def calc_fall_flush_timings_durations(flow_matrix, summer_timings):
    max_zero_allowed_per_year = fall_params['max_zero_allowed_per_year']
    max_nan_allowed_per_year = fall_params['max_nan_allowed_per_year']
    min_flow_rate = fall_params['min_flow_rate']
    sigma = fall_params['sigma'] # Smaller filter to find fall flush peak
    wet_sigma = fall_params['wet_sigma'] # Larger filter to find wet season peak
    peak_sensitivity = fall_params['peak_sensitivity'] # smaller is more peak
    max_flush_duration = fall_params['max_flush_duration'] # Maximum duration from start to end, for fall flush peak
    wet_threshold_perc = fall_params['wet_threshold_perc'] # Return to wet season flow must be certain percentage of that year's max flow
    flush_threshold_perc = fall_params['flush_threshold_perc'] # Size of flush peak, from rising limb to top of peak, has great enough change
    min_flush_threshold = fall_params['min_flush_threshold']
    date_cutoff = fall_params['date_cutoff'] # Latest accepted date for fall flush, in Julian Date counting from Oct 1st = 0. (i.e. Dec 15th = 75)

    start_dates = []
    wet_dates = []
    durations = []
    mags = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        start_dates.append(None)
        wet_dates.append(None)
        durations.append(None)
        mags.append(None)

        """Check to see if water year has more than allowed nan or zeros"""
        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year or max(flow_matrix[:, column_number]) < min_flow_rate:
            continue;

        """Get flow data"""
        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Interpolate between None values"""
        flow_data = replace_nan(flow_data)

        """Return to Wet Season"""
        wet_filter_data = gaussian_filter1d(flow_data, wet_sigma)
        return_date = return_to_wet_date(wet_filter_data, wet_threshold_perc)
        wet_dates[-1] = return_date + 10

        """Filter noise data with small sigma to find fall flush hump"""
        filter_data = gaussian_filter1d(flow_data, sigma)

        """Fit spline"""
        x_axis = list(range(len(filter_data)))
        spl = ip.UnivariateSpline(x_axis, filter_data, k=3, s=3)

        """Find the peaks and valleys of the filtered data"""
        mean_flow = np.nanmean(filter_data)
        maxarray, minarray = peakdet(spl(x_axis), mean_flow * peak_sensitivity)

        """Find max and min of filtered flow data"""
        max_flow = max(filter_data[20:])
        max_flow_index = find_index(filter_data[20:], max_flow) + 20
        min_flow = min(wet_filter_data[:max_flow_index])

        """If could not find any max and find"""
        if not list(maxarray) or not list(minarray) or minarray[0][0] > max_flow_index:
            continue;

        """Get flow magnitude threshold from previous summer's baseflow"""
        baseflows = []
        if column_number == 0:
            wet_date = wet_dates[0]
            baseflow = list(flow_matrix[:wet_date, column_number])
            bs_mean = np.mean(baseflow)
            bs_med = np.nanpercentile(baseflow, 50)
        else:
            summer_date = summer_timings[column_number -1]
            if wet_dates[column_number] > 20:
                wet_date = wet_dates[column_number] - 20
            baseflow = list(flow_matrix[summer_date:,column_number -1]) + list(flow_matrix[:wet_date, column_number])
            bs_mean = np.mean(baseflow)
            bs_med = np.nanpercentile(baseflow, 50)

        """Get fall flush peak"""
        counter = 0
        half_duration = int(max_flush_duration/2) # Only test duration for first half of fall flush peak
        if bs_med > 25:
            min_flush_magnitude = bs_med * 1.5 # if median baseflow is large (>25), magnitude threshold is 50% above median baseflow of previous summer
        else:
            min_flush_magnitude = bs_med * 2 # otherwise magnitude threshold is 100% above median baseflow of previous summer
        if min_flush_magnitude < min_flush_threshold:
            min_flush_magnitude = min_flush_threshold
        for flow_index in maxarray:

            if counter == 0:
                if flow_index[0] < half_duration and flow_index[0] != 0 and flow_index[1] > wet_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude:
                    """if index found is before the half duration allowed"""
                    start_dates[-1]=int(flow_index[0])
                    mags[-1]=flow_index[1]
                    break
                elif bool((flow_index[1] - spl(maxarray[counter][0] - half_duration)) / flow_index[1] > flush_threshold_perc or minarray[counter][0] - maxarray[counter][0] < half_duration) and flow_index[1] > wet_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude:
                    """If peak and valley is separted by half duration, or half duration to the left is less than 30% of its value"""
                    start_dates[-1]=int(flow_index[0])
                    mags[-1]=flow_index[1]
                    break
            elif counter == len(minarray):
                start_dates[-1]=None
                mags[-1]=None
                break;
            elif bool(minarray[counter][0] - maxarray[counter][0] < half_duration or maxarray[counter][0] - minarray[counter-1][0] < half_duration) and bool(flow_index[1] > wet_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff):
                """valley and peak are distanced by less than half dur from either side"""
                start_dates[-1]=int(flow_index[0])
                mags[-1]=flow_index[1]
                break
            elif (spl(flow_index[0] - half_duration) - min_flow) / (flow_index[1] - min_flow) < flush_threshold_perc and (spl(flow_index[0] + half_duration) - min_flow) / (flow_index[1] - min_flow) < flush_threshold_perc and flow_index[1] > wet_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff:
                """both side of flow value at the peak + half duration index fall below flush_threshold_perc"""
                start_dates[-1]=int(flow_index[0])
                mags[-1]=flow_index[1]
                break
            counter = counter + 1

        """Check to see if last start_date falls behind the max_allowed_date"""
        if bool(start_dates[-1] is None or start_dates[-1] > wet_dates[-1]) and wet_dates[-1]:
            start_dates[-1] = None
            mags[-1] = None

        """Get duration of each fall flush"""
        current_duration, left, right = calc_fall_flush_durations_2(filter_data, start_dates[-1])
        durations[-1] = current_duration
        #_plotter(x_axis, flow_data, filter_data, wet_filter_data, start_dates, wet_dates, column_number, left, right, maxarray, minarray, min_flush_magnitude)

    return start_dates, mags, wet_dates, durations

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

    """Left side sharp"""
    der_percent_threshold_left = 50 # Slope of rising limb (i.e. derivative) must be "sharp"
    flow_percent_threshold_left = 80

    """Right side mellow"""
    der_percent_threshold_right = 30 # Slope of falling limb (i.e. derivative) has lower requirement to be part of flush duration
    flow_percent_threshold_right = 80

    duration = None
    left = 0
    right = 0

    if date or date == 0:
        date = int(date)
        left_maxarray, left_minarray = peakdet(filter_data[:date], 0.01)
        right_maxarray, right_minarray = peakdet(filter_data[date:], 0.01)

        if not list(left_minarray):
            left = 0
        else:
            left = int(left_minarray[-1][0])

        if not list(right_minarray):
            right = 0
        else:
            right = int(date - 2 + right_minarray[0][0])

        if date - left > 10:
            """create spline, and find derivative"""
            x_axis_left = list(range(len(filter_data[left:date])))
            spl_left = ip.UnivariateSpline(x_axis_left, filter_data[left:date], k=3, s=3)
            spl_first_left = spl_left.derivative(1)

            """check if derivative value falls below certain threshold"""
            spl_first_left_median = np.nanpercentile(spl_first_left(x_axis_left), der_percent_threshold_left)

            """check if actual value falls below threshold, avoiding the rounded peak"""
            median_left = np.nanpercentile(list(set(filter_data[left:date])), flow_percent_threshold_left)

            for index_left, der in enumerate(reversed(spl_first_left(x_axis_left))):
                # print(der < spl_first_left_median, filter_data[date - index_left] < median_left)
                if der < spl_first_left_median and filter_data[date - index_left] < median_left:
                    left = date - index_left
                    break

        if right - date > 10:
            x_axis_right = list(range(len(filter_data[date:right])))
            spl_right = ip.UnivariateSpline(x_axis_right, filter_data[date:right], k=3, s=3)
            spl_first_right = spl_right.derivative(1)

            spl_first_right_median = abs(np.nanpercentile(spl_first_right(x_axis_right), der_percent_threshold_right))
            median_right = np.nanpercentile(list(set(filter_data[date:right])), flow_percent_threshold_right)

            for index_right, der in enumerate(spl_first_right(x_axis_right)):
                # print(date+index_right, der < spl_first_right_median, filter_data[date + index_right] < median_right)
                if abs(der) < spl_first_right_median and filter_data[date + index_right] < median_right:
                    right = date + index_right
                    break

        if left:
            duration = int(date - left)
        elif not left and right:
            duration = int(right - date)
        else:
            duration = 0

    return duration, left, right


def return_to_wet_date(wet_filter_data, wet_threshold_perc):
    max_wet_peak_mag = max(wet_filter_data[20:])
    max_wet_peak_index = find_index(wet_filter_data, max_wet_peak_mag)
    min_wet_peak_mag = min(wet_filter_data[:max_wet_peak_index])
    """Loop backwards from max flow index to beginning, to search for wet season"""
    for index, value in enumerate(reversed(wet_filter_data[:max_wet_peak_index])):
        if index == len(wet_filter_data[:max_wet_peak_index] - 1):
            return None
        elif (value - min_wet_peak_mag) / (max_wet_peak_mag - min_wet_peak_mag) < wet_threshold_perc:
            """If value percentage falls below wet_threshold_perc"""
            return_date = max_wet_peak_index - index
            return return_date

def _plotter(x_axis, flow_data, filter_data, wet_filter_data, start_dates, wet_dates, column_number, left, right, maxarray, minarray, min_flush_magnitude):
    plt.figure()
    plt.plot(x_axis, flow_data, '.')
    plt.plot(x_axis, filter_data)
    #plt.plot(x_axis, wet_filter_data)
    # for data in maxarray:
    #     plt.plot(data[0], data[1], '^')
    # for data in minarray:
    #     plt.plot(data[0], data[1], 'v')
    if start_dates[-1] is not None:
        plt.axvline(start_dates[-1], color='blue')
    plt.axvline(wet_dates[-1], color="green")
    #plt.axvline(left, ls=":")
    #plt.axvline(right, ls=":")
    if min_flush_magnitude is not None:
        plt.axhline(min_flush_magnitude, ls='--', color = 'red')
    #plt.yscale('log')
    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
