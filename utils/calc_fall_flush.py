import numpy as np
import scipy.interpolate as ip
# import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from utils.helpers import find_index, peakdet, replace_nan
from params import fall_params as def_fall_params
from utils.helpers import set_user_params


def calc_fall_flush_timings_durations(flow_matrix, summer_timings, class_number, fall_params=def_fall_params):
    params = set_user_params(fall_params, def_fall_params)

    max_zero_allowed_per_year, max_nan_allowed_per_year, min_flow_rate, sigma, broad_sigma, wet_season_sigma, peak_sensitivity, peak_sensitivity_wet, max_flush_duration, min_flush_percentage, wet_threshold_perc, peak_detect_perc, flush_threshold_perc, min_flush_threshold, date_cutoff, slope_sensitivity = params.values()

    start_dates = []
    wet_dates = []
    durations = []
    mags = []

    for column_number, _ in enumerate(flow_matrix[0]):

        start_dates.append(None)
        wet_dates.append(None)
        durations.append(None)
        mags.append(None)

        """Check to see if water year has more than allowed nan or zeros"""
        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number] == 0) > max_zero_allowed_per_year or max(flow_matrix[:, column_number]) < min_flow_rate:
            continue

        """Get flow data"""
        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Interpolate between None values"""
        flow_data = replace_nan(flow_data)

        """Return to Wet Season"""
        if class_number == 3 or class_number == 4 or class_number == 5 or class_number == 6 or class_number == 7 or class_number == 8:
            wet_season_filter_data = gaussian_filter1d(flow_data, 6)
        else:
            wet_season_filter_data = gaussian_filter1d(flow_data, wet_season_sigma)
        broad_filter_data = gaussian_filter1d(flow_data, broad_sigma)
        if class_number == 1 or class_number == 2 or class_number == 9:
            slope_detection_data = gaussian_filter1d(flow_data, 7)
        elif class_number == 3 or class_number == 4 or class_number == 5 or class_number == 6 or class_number == 7 or class_number == 8: 
            slope_detection_data = gaussian_filter1d(flow_data, 1)
        else:
            slope_detection_data = gaussian_filter1d(flow_data, 4)

        return_date = return_to_wet_date(flow_data, wet_season_filter_data, broad_filter_data, slope_detection_data, 
                                         wet_threshold_perc, peak_detect_perc, peak_sensitivity_wet, column_number, slope_sensitivity)
        if return_date:
            wet_dates[-1] = return_date 
        broad_filter_data = gaussian_filter1d(flow_data, broad_sigma)

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

        min_flow = min(broad_filter_data[:max_flow_index])

        """If could not find any max and find"""
        if not list(maxarray) or not list(minarray) or minarray[0][0] > max_flow_index:
            continue

        """Get flow magnitude threshold from previous summer's baseflow"""
        if column_number == 0:
            wet_date = wet_dates[0]
            baseflow = list(flow_matrix[:wet_date, column_number])
            # bs_mean = np.mean(baseflow)
            bs_med = np.nanpercentile(baseflow, 50)
        else:
            summer_date = summer_timings[column_number - 1]
            if wet_dates[column_number]:
                if wet_dates[column_number] > 20:
                    wet_date = wet_dates[column_number] - 20
                else:
                    wet_date = wet_dates[column_number]
                baseflow = list(flow_matrix[summer_date:, column_number - 1]) + list(flow_matrix[:wet_date, column_number])
                # bs_mean = np.mean(baseflow)
            else:
                baseflow = list(flow_matrix[summer_date:, column_number - 1])
            bs_med = np.nanpercentile(baseflow, 50)

        """Get fall flush peak"""
        counter = 0
        # Only test duration for first half of fall flush peak
        half_duration = int(max_flush_duration/2)
        if bs_med > 25:
            # if median baseflow is large (>25), magnitude threshold is 50% above median baseflow of previous summer
            min_flush_magnitude = bs_med * 1.5
        else:
            # otherwise magnitude threshold is 100% above median baseflow of previous summer
            min_flush_magnitude = bs_med * 2
        if min_flush_magnitude < min_flush_threshold:
            min_flush_magnitude = min_flush_threshold
        for flow_index in maxarray:

            if counter == 0:
                if flow_index[0] < half_duration and flow_index[0] != 0 and flow_index[1] > broad_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff:
                    """if index found is before the half duration allowed"""
                    start_dates[-1] = int(flow_index[0])
                    mags[-1] = flow_index[1]
                    break
                elif bool((flow_index[1] - spl(maxarray[counter][0] - half_duration)) / flow_index[1] > flush_threshold_perc or minarray[counter][0] - maxarray[counter][0] < half_duration) and flow_index[1] > broad_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff:
                    """If peak and valley is separted by half duration, or half duration to the left is less than 30% of its value"""
                    start_dates[-1] = int(flow_index[0])
                    mags[-1] = flow_index[1]
                    break
            elif counter == len(minarray):
                start_dates[-1] = None
                mags[-1] = None
                break
            elif bool(minarray[counter][0] - maxarray[counter][0] < half_duration or maxarray[counter][0] - minarray[counter-1][0] < half_duration) and bool(flow_index[1] > broad_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff):
                """valley and peak are distanced by less than half dur from either side"""
                start_dates[-1] = int(flow_index[0])
                mags[-1] = flow_index[1]
                break
            elif (spl(flow_index[0] - half_duration) - min_flow) / (flow_index[1] - min_flow) < flush_threshold_perc and (spl(flow_index[0] + half_duration) - min_flow) / (flow_index[1] - min_flow) < flush_threshold_perc and flow_index[1] > broad_filter_data[int(flow_index[0])] and flow_index[1] > min_flush_magnitude and flow_index[0] <= date_cutoff:
                """both side of flow value at the peak + half duration index fall below flush_threshold_perc"""
                start_dates[-1] = int(flow_index[0])
                mags[-1] = flow_index[1]
                break
            counter = counter + 1

        """Check to see if last start_date falls behind the max_allowed_date"""
        if wet_dates[-1]:
            if bool(start_dates[-1] is None or start_dates[-1] > wet_dates[-1]) and wet_dates[-1]:
                start_dates[-1] = None
                mags[-1] = None

        """Get duration of each fall flush"""
        current_duration, left, right = calc_fall_flush_durations_2(
            filter_data, start_dates[-1])
        durations[-1] = current_duration
        # _plotter(x_axis, flow_data, filter_data, broad_filter_data, start_dates, wet_dates, column_number, left, right, maxarray, minarray, min_flush_magnitude, slope_detection_data)
        
    return start_dates, mags, wet_dates, durations


def calc_fall_flush_durations(flow_data, broad_filter_data, date):

    duration_left = None
    duration_right = None
    duration = None

    if date:
        date = int(date)
        for index_left, flow_left in enumerate(reversed(flow_data[:date])):
            if flow_left < broad_filter_data[date - index_left]:
                duration_left = index_left
                break
        for index_right, flow_right in enumerate(flow_data[date:]):
            if flow_right < broad_filter_data[date + index_right]:
                duration_right = index_right
                break

        if duration_left and duration_right:
            duration = duration_left + duration_right
        else:
            duration = None

    return duration


def calc_fall_flush_durations_2(filter_data, date):
    """Left side sharp"""
    der_percent_threshold_left = 50  # Slope of rising limb (i.e. derivative) must be "sharp"
    flow_percent_threshold_left = 80

    """Right side mellow"""
    der_percent_threshold_right = 30  # Slope of falling limb (i.e. derivative) has lower requirement to be part of flush duration
    flow_percent_threshold_right = 80

    duration = None
    left = 0
    right = 0

    if date or date == 0:
        date = int(date)
        _, left_minarray = peakdet(filter_data[:date], 0.01)
        _, right_minarray = peakdet(filter_data[date:], 0.01)

        if not list(left_minarray):
            left = 0
        else:
            left = int(left_minarray[-1][0])

        if not list(right_minarray):
            right = 0
        else:
            right = int(date + right_minarray[0][0])

        if date - left > 10:
            """create spline, and find derivative"""
            x_axis_left = list(range(len(filter_data[left:date])))
            spl_left = ip.UnivariateSpline(
                x_axis_left, filter_data[left:date], k=3, s=3)
            spl_first_left = spl_left.derivative(1)

            """check if derivative value falls below certain threshold"""
            spl_first_left_median = np.nanpercentile(
                spl_first_left(x_axis_left), der_percent_threshold_left)

            """check if actual value falls below threshold, avoiding the rounded peak"""
            median_left = np.nanpercentile(
                list(set(filter_data[left:date])), flow_percent_threshold_left)

            for index_left, der in enumerate(reversed(spl_first_left(x_axis_left))):
                # print(der < spl_first_left_median, filter_data[date - index_left] < median_left)
                if der < spl_first_left_median and filter_data[date - index_left] < median_left:
                    left = date - index_left
                    break

        if right - date > 10:
            x_axis_right = list(range(len(filter_data[date:right])))
            spl_right = ip.UnivariateSpline(
                x_axis_right, filter_data[date:right], k=3, s=3)
            spl_first_right = spl_right.derivative(1)

            spl_first_right_median = abs(np.nanpercentile(
                spl_first_right(x_axis_right), der_percent_threshold_right))
            median_right = np.nanpercentile(
                list(set(filter_data[date:right])), flow_percent_threshold_right)

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


def return_to_wet_date(flow_data, wet_season_filter_data, broad_filter_data, slope_detection_data, wet_threshold_perc, peak_detect_perc, peak_sensitivity_wet, column_number, slope_sensitivity):
    search_index = None
    max_wet_peak_mag = max(broad_filter_data[20:])
    max_wet_peak_index = find_index(broad_filter_data, max_wet_peak_mag)

    if broad_filter_data[:max_wet_peak_index].size == 0:
        return None
    min_wet_peak_mag = min(broad_filter_data[:max_wet_peak_index])
    maxarray_wet, _ = peakdet(
        wet_season_filter_data, peak_sensitivity_wet)

    """Get the derivative of smoothed data for rate of change requirement"""
    x_axis = list(range(len(slope_detection_data)))
    spl = ip.UnivariateSpline(x_axis, slope_detection_data, k=3, s=3)
    spl_first = spl.derivative(n=1)

    """Loop through peaks to find starting point of search"""
    for index, value in enumerate(maxarray_wet):
        if len(maxarray_wet) == 1:
            if maxarray_wet[0][0] == 0:
                search_index = max_wet_peak_index
                break
            else:
                search_index = int(maxarray_wet[0][0])
                break
        else:
            if (maxarray_wet[index][1]-min_wet_peak_mag)/(max_wet_peak_mag-min_wet_peak_mag) > peak_detect_perc:
                search_index = int(maxarray_wet[index][0])
                break
    """Loop backwards from max flow index to beginning, to search for wet season"""
    if not search_index:
        return None
    for index, value in enumerate(reversed(wet_season_filter_data[:search_index])):
        if index == len(wet_season_filter_data[:search_index] - 1):
            return None
        elif (value - min_wet_peak_mag) / (max_wet_peak_mag - min_wet_peak_mag) < wet_threshold_perc and abs(spl_first(search_index - index)) < max_wet_peak_mag/slope_sensitivity:
            """If value percentage falls below wet_threshold_perc"""
            return_date = search_index - index
            
            # plt.figure()
            # plt.plot(flow_data, '-', slope_detection_data, '--')
            # if return_date is not None:
            #     plt.axvline(return_date, color='blue')
            # plt.axhline((max_wet_peak_mag-min_wet_peak_mag)*.2, color='orange')
            # plt.text(364,max(flow_data),str(abs(spl_first(search_index - index))))
            # plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))

            return return_date
            

def _plotter(x_axis, flow_data, filter_data, broad_filter_data, start_dates, wet_dates, column_number, left, right, maxarray, minarray, min_flush_magnitude, slope_detection_data):
    plt.figure()
    plt.plot(x_axis, flow_data)
    #plt.plot(x_axis, filter_data)
    plt.plot(x_axis, slope_detection_data, color='orange')
    # for data in maxarray:
    #     plt.plot(data[0], data[1], '^')
    # for data in minarray:
    #     plt.plot(data[0], data[1], 'v')
    if wet_dates[-1] is not None:
        plt.axvline(wet_dates[-1], color='blue')
    #plt.axvline(wet_dates[-1], color="green")
    #plt.axvline(left, ls=":")
    #plt.axvline(right, ls=":")
    # if min_flush_magnitude is not None:
    #     plt.axhline(min_flush_magnitude, ls='--', color = 'red')
    #plt.yscale('log')
    
    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
