import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from scipy.ndimage import gaussian_filter1d
from utils.helpers import find_index, peakdet, replace_nan
from params import summer_params

def calc_start_of_summer(matrix):
    """Set adjustable parameters for start of summer date detection"""
    max_zero_allowed_per_year = summer_params['max_zero_allowed_per_year']
    max_nan_allowed_per_year = summer_params['max_nan_allowed_per_year']
    sigma = summer_params['sigma'] # determines amount of smoothing for summer timing detection
    sensitivity = summer_params['sensitivity'] # increased sensitivity returns smaller threshold for derivative
    peak_sensitivity = summer_params['peak_sensitivity'] # identifies last major peak after which to search for start date
    max_peak_flow_date = summer_params['max_peak_flow_date'] # max search date for the peak flow date
    min_summer_flow_percent = summer_params['min_summer_flow_percent'] # require that summer start is below this flow threshold

    start_dates = []
    for column_number, flow_data in enumerate(matrix[0]):
        start_dates.append(None)
        """Check if data has too many zeros or NaN, and if so skip to next water year"""
        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number]==0) > max_zero_allowed_per_year:
            continue;

        """Append each column with 30 more days from next column, except the last column"""
        if column_number != len(matrix[0])-1:
            flow_data = list(matrix[:,column_number]) + list(matrix[:100,column_number+1])
        else:
            flow_data = matrix[:, column_number]

        """Replace any NaNs with previous day's flow"""
        flow_data = replace_nan(flow_data)

        """Smooth out the timeseries"""
        smooth_data = gaussian_filter1d(flow_data, sigma)
        x_axis = list(range(len(smooth_data)))

        """Find spline fit equation for smoothed timeseries, and find derivative of spline"""
        spl = ip.UnivariateSpline(x_axis, smooth_data, k=3, s=3)
        spl_first = spl.derivative(1)

        max_flow_data = max(smooth_data[:366])
        max_flow_index = find_index(smooth_data, max_flow_data)

        """Find the major peaks of the filtered data"""
        mean_flow = np.nanmean(flow_data)
        maxarray, minarray = peakdet(smooth_data, mean_flow * peak_sensitivity)
        """Set search range after last smoothed peak flow"""
        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date:
                max_flow_index = int(flow_index[0])
                break

        """Set a magnitude threshold below which start of summer can begin"""
        min_flow_data = min(smooth_data[max_flow_index:366])
        threshold = min_flow_data + (smooth_data[max_flow_index] - min_flow_data) * min_summer_flow_percent

        current_sensitivity = 1/sensitivity
        start_dates[-1] = None
        for index, data in enumerate(smooth_data):
            if index == len(smooth_data)-2:
                break
            """Search criteria: derivative is under rate of change threshold, date is after last major peak, and flow is less than specified percent of smoothed max flow"""
            if abs(spl_first(index)) < max_flow_data * current_sensitivity and index > max_flow_index and data < threshold:
                start_dates[-1] = index
                break

        # _summer_baseflow_plot(x_axis, column_number, flow_data, spl, spl_first, start_dates, threshold, max_flow_index, maxarray)

    return start_dates

def calc_summer_baseflow_durations_magnitude(flow_matrix, summer_start_dates, fall_flush_dates, fall_flush_wet_dates):
    summer_10_magnitudes = []
    summer_50_magnitudes = []
    summer_flush_durations = []
    summer_wet_durations = []
    summer_no_flow_counts = []

    for column_number, summer_start_date in enumerate(summer_start_dates):
        if column_number == len(summer_start_dates) - 1:
            if not np.isnan(summer_start_date) and not np.isnan(fall_flush_wet_dates[column_number]):
                su_date = int(summer_start_date)
                wet_date = int(fall_flush_wet_dates[column_number])
                if not np.isnan(fall_flush_dates[column_number]):
                    fl_date = int(fall_flush_dates[column_number])
                    flow_data_flush = list(flow_matrix[su_date:,column_number]) + list(flow_matrix[:fl_date, column_number])
                if not np.isnan(fall_flush_wet_dates[column_number]):
                    flow_data_wet = list(flow_matrix[su_date:,column_number]) + list(flow_matrix[:wet_date, column_number])
            else:
                flow_data_flush = None
                flow_data_wet = None
        else:
            if not np.isnan(summer_start_date) and not np.isnan(fall_flush_wet_dates[column_number + 1]):
                su_date = int(summer_start_date)
                wet_date = int(fall_flush_wet_dates[column_number + 1])
                flow_data_flush = None
                if not np.isnan(fall_flush_dates[column_number + 1]):
                    fl_date = int(fall_flush_dates[column_number + 1])
                    flow_data_flush = list(flow_matrix[su_date:,column_number]) + list(flow_matrix[:fl_date, column_number + 1])
                if not np.isnan(fall_flush_wet_dates[column_number + 1]):
                    flow_data_wet = list(flow_matrix[su_date:,column_number]) + list(flow_matrix[:wet_date, column_number + 1])
            else:
                flow_data_flush = None
                flow_data_wet = None

        if flow_data_flush and flow_data_wet:
            summer_10_magnitudes.append(np.nanpercentile(flow_data_wet, 10))
            summer_50_magnitudes.append(np.nanpercentile(flow_data_wet, 50))
            summer_flush_durations.append(len(flow_data_flush))
            summer_wet_durations.append(len(flow_data_wet))
            summer_no_flow_counts.append(len(flow_data_wet) - np.count_nonzero(flow_data_wet))
        elif not flow_data_flush and flow_data_wet:
            summer_10_magnitudes.append(np.nanpercentile(flow_data_wet, 10))
            summer_50_magnitudes.append(np.nanpercentile(flow_data_wet, 50))
            summer_flush_durations.append(None)
            summer_wet_durations.append(len(flow_data_wet))
            summer_no_flow_counts.append(len(flow_data_wet) - np.count_nonzero(flow_data_wet))
        else:
            summer_10_magnitudes.append(None)
            summer_50_magnitudes.append(None)
            summer_flush_durations.append(None)
            summer_wet_durations.append(None)
            summer_no_flow_counts.append(None)

    return summer_10_magnitudes, summer_50_magnitudes, summer_flush_durations, summer_wet_durations, summer_no_flow_counts

def _summer_baseflow_plot(x_axis, column_number, flow_data, spl, spl_first, start_dates, threshold, max_flow_index, maxarray):

    plt.figure(column_number)

    plt.plot(x_axis, spl_first(x_axis), color='red') #spl 1st derivative
    plt.plot(flow_data, '-', color='blue') #raw
    plt.plot(x_axis, spl(x_axis),'--', color='orange') #spline
    plt.title('Start of Summer Metric')
    plt.xlabel('Julian Day')
    plt.ylabel('Flow, ft^3/s')
    if start_dates[-1] is not None:
        plt.axvline(start_dates[-1], color='red')
    plt.axhline(threshold, color = 'green')
    plt.axvline(max_flow_index, ls=':')
    for data in maxarray:
        plt.plot(data[0], data[1], '^')

    plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))
