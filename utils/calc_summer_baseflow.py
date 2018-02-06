import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as ip
from utils.helpers import moving_average, get_nan_fraction_in_array
from utils.helpers import find_index, peakdet
from scipy.ndimage import gaussian_filter1d

def calc_start_of_summer(matrix):

    """Define function parameters"""
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36
    filter_maxflow = 7 # scalar to set amount of smoothing
    sensitivity = 900 # increased sensitivity returns smaller threshold for derivative
    peak_sensitivity = .2 # identifies last major peak after which to search for start date.
    max_peak_flow_date = 300 # max search date for the peak flow date
    percent_final = .05 # Ensure that the flow during the summer start date is under 5th percentile

    start_dates = []
    for column_number, flow in enumerate(matrix[0]):
        """Check if data has too many zeros or NaN, and if so skip to next water year"""
        if np.isnan(matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(matrix[:, column_number]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            continue;

        """Append each column with 30 more days from next column, except the last column"""
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

        """Smooth out the timeseries"""
        smooth_data = gaussian_filter1d(flow_data, filter_maxflow)
        x_axis = list(range(len(smooth_data)))

        """Find spline fit equation for smoothed timeseries, and find derivative of spline"""
        spl = ip.UnivariateSpline(x_axis, smooth_data, k=3, s=3)
        spl_first = spl.derivative(1)

        max_flow_data = max(smooth_data)
        max_flow_index = find_index(smooth_data, max_flow_data)

        """Find the major peaks of the filtered data"""
        mean_flow = np.nanmean(flow_data)
        maxarray, minarray = peakdet(smooth_data, mean_flow * peak_sensitivity)
        """Set search range after last smoothed out peak flow"""
        for flow_index in reversed(maxarray):
            if int(flow_index[0]) < max_peak_flow_date:
                max_flow_index = int(flow_index[0])
                break

        current_sensitivity = 1/sensitivity
        start_dates.append(0)
        for index, data in enumerate(smooth_data):
            if index == len(smooth_data)-2:
                break
            """Search criteria: derivative is under threshold for two days, date is after last major peak, and flow is within specified percent of smoothed max flow"""
            if abs(spl_first(index)) < max_flow_data * current_sensitivity and \
            abs(spl_first(index+1)) < max_flow_data * current_sensitivity and index > max_flow_index and \
            data < max_flow_data * percent_final:
                start_dates[-1] = index
                break

        #_summer_baseflow_plot(x_axis, column_number, flow_data, smooth_data, spl_first, start_dates)

    return start_dates

def _summer_baseflow_plot(x_axis, column_number, flow_data, smooth_data, spl_first, start_dates):

    plt.figure(column_number)

    plt.plot(x_axis, spl_first(x_axis), color='red') #spl 1st derivative
    plt.plot(flow_data, '-', color='blue') #raw
    plt.plot(x_axis, spl(x_axis),'--', color='orange') #spline
    plt.title('Start of Summer Metric')
    plt.xlabel('Julian Day')
    plt.ylabel('Flow, ft^3/s')
    plt.axvline(start_dates[-1], color='red')
    plt.axvline(max_flow_index, color='yellow')

    plt.savefig('post_processedFiles/Summer_baseflow/{}.png'.format(column_number+1))
