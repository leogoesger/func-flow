import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from utils.helpers import moving_average, get_nan_fraction_in_array
from utils.helpers import find_index, peakdet
from scipy.ndimage import gaussian_filter1d

def calc_start_of_summer(matrix):

    """Define the allowable number of zeros or Nans to go ahead and process data"""
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    """Define the amount of smoothing for filters to identify the annual max, and for identifying start date of summer"""
    filter_maxflow = 7
    sensitivity = 900
    peak_sensitivity = .2
    max_peak_flow_date = 300 # max search date for the peak flow date
    percent_final = .5 # Ensure that the flow during the summer start date is under 5th percentile

    start_dates = []
    for column_number, flow in enumerate(matrix[0]):
        """Check if data has too many zeros or NaN, and if so skip to next water year"""
        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            continue;

        """Append each column with more data from next column, except the last column"""
        if column_number != len(matrix[0])-1:
            flow_data = list(matrix[:,column_number]) + list(matrix[:30,column_number+1])
        else:
            flow_data = matrix[:, column_number]

        """Replace any NaNs with previous day's flow"""
        for index, flow in enumerate(flow_data):
            if index == 0 and np.isnan(flow) == True:
                flow_data[index] = 0
            elif index > 0 and np.isnan(flow) == True:
                flow_data[index] = flow_data[index-1]

        """Smooth out the timeseries and set search range after last smoothed out peak flow"""
        smooth_data = gaussian_filter1d(flow_data, filter_maxflow)
        x_axis = list(range(len(smooth_data)))

        spl = ip.UnivariateSpline(x_axis, smooth_data, k=3, s=3)
        spl_first = spl.derivative(1)

        max_flow_data = max(smooth_data)
        max_flow_index = find_index(smooth_data, max_flow_data)

        """Find the peaks and valleys of the filtered data"""
        mean_flow = np.nanmean(flow_data)
        maxarray, minarray = peakdet(smooth_data, mean_flow * peak_sensitivity)
        """Find the rightmost peak that doesn't exceed max allowed peak date"""
        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date:
                max_flow_index = int(flow_index[0])
                break

        current_sensitivity = 1/sensitivity
        start_dates.append(0)
        for index, data in enumerate(smooth_data):
            if index == len(smooth_data)-2:
                break
            """Search criteria: derivative is under threshold for two days, date is after last major peak, and flow is within 5 percent of smoothed max flow"""
            if abs(spl_first(index)) < max_flow_data * current_sensitivity and \
            abs(spl_first(index+1)) < max_flow_data * current_sensitivity and index > max_flow_index and \
            data < max_flow_data * percent_final):
                start_dates[-1] = index
                break

        plt.figure(column_number)
        plt.plot(x_axis, smooth_data, 'x')   #smoothed
        plt.plot(x_axis, spl(x_axis))
        plt.plot(x_axis, spl_first(x_axis)) #spl 1st
        plt.plot(flow_data, '-') #raw
        plt.title('Start of Summer Metric')
        plt.xlabel('Julian Day')
        plt.ylabel('Flow, ft^3/s')
        plt.axvline(start_dates[-1], color='red')
        plt.axvline(max_flow_index, color='purple')

        plt.savefig('post_processedFiles/Summer_baseflow/{}.png'.format(column_number+1))

    return start_dates


def calc_start_of_summer_noelle(matrix):

    """Define the allowable number of zeros or Nans to go ahead and process data"""
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    """Define the amount of smoothing for filters to identify the annual max, and for identifying start date of summer"""
    filter_maxflow = 7
    filter_dailyflow = 3

    start_dates = []

    for column_number, flow in enumerate(matrix[0]):
        """Check if data has too many zeros or NaN, and if so skip to next water year"""
        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            continue;

        """Append each column with more data from next column, except the last column"""
        if column_number != len(matrix[0])-1:
            flow_data = matrix[:,column_number] + matrix[:30,column_number+1]
        else:
            flow_data = matrix[:, column_number]

        """Filter data"""

        """Smooth out the timeseries and set search range after smoothed out max flow"""
        smooth_data_max = gaussian_filter1d(flow_data, filter_maxflow)
        search_range = find_index(smooth_data_max, max(smooth_data_max))
        if not search_range:
            start_dates.append(None)
            continue;

        smooth_data = gaussian_filter1d(matrix[:,index], filter_dailyflow)
        spl = ip.UnivariateSpline(x_axis_window, flow_data_window, k=3, s=3)
        spl_first = spl.derivative(1)
        for data_index, data in enumerate(smooth_data):

            """For a low flow percentile <=1 cfs, only require smoothed flow to stay at or under threshold for two days"""
            if percentile <= 1:
                if (data_index > len(smooth_data) - 2):
                    start_dates.append(None)
                    break
                elif data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile:
                    start_dates.append(data_index)
            else:
                """When the low flow percentile is above zero, require smoothed flow to stay at or under threshold for four days"""
                if (data_index > len(smooth_data) - 4):
                    start_dates.append(None)
                    break
                if data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile and smooth_data[data_index + 3] <= percentile:
                    start_dates.append(data_index)
                    break

        """Consider test failed if start data is calculated right on the search range or as zero"""
        if start_dates[index] == search_range:
            start_dates[index] = None
        elif start_dates[index] == 0:
            start_dates[index] = None

        #_summer_baseflow_plot(index, matrix, smooth_data, start_dates, percentile, search_range)


    return start_dates

def _summer_baseflow_plot(x_axis, column_number, flow_data, smooth_data, spl_first, start_dates):

    plt.figure(column_number)
    plt.plot(x_axis, flow_data, '-') #raw
    plt.plot(x_axis, smooth_data)   #smoothed
    plt.plot(x_axis, spl_first(x_axis)) #spl 1st
    plt.title('Start of Summer Metric')
    plt.xlabel('Julian Day')
    plt.ylabel('Flow, ft^3/s')
    plt.axvline(start_dates, color='red')

    plt.savefig('post_processedFiles/Summer_baseflow/{}.png'.format(column_number+1))
