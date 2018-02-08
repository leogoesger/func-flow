import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def calc_fall_flush_timing_duration(flow_matrix, start_of_summer):
    max_zero_allowed_per_year = 120
    max_nan_allowed_per_year = 36

    sigma = 10
    start_dates = []
    fall_flush_duration = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        if np.isnan(flow_matrix[:, column_number]).sum() > max_nan_allowed_per_year or np.count_nonzero(flow_matrix[:, column_number]==0) > max_zero_allowed_per_year:
            start_dates.append(None)
            fall_flush_duration.append(None)
            continue;

        """Summer baseflow determined by the previous year if not the first year"""
        if column_number == 0:
            if np.isnan(start_of_summer[0]):
                start_dates.append(None)
                fall_flush_duration.append(None)
                continue
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[ int(start_of_summer[0]) : 361, 0])
        elif np.isnan(start_of_summer[column_number - 1]):
            start_dates.append(None)
            fall_flush_duration.append(None)
            continue
        elif start_of_summer[column_number - 1] > 366:
            summer_flow = flow_matrix[int(start_of_summer[column_number - 1]) - 366 : int(start_of_summer[column_number - 1]) - 346, column_number]
            summer_baseflow = 1.5 * np.nanmedian(summer_flow)
        else:
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[int(start_of_summer[column_number - 1]):361, column_number - 1])

        print(column_number)
        print(summer_baseflow)
        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        for index, flow in enumerate(flow_data):
            if index == 0 and np.isnan(flow):
                flow_data[index] = 0
            elif index > 0 and np.isnan(flow):
                flow_data[index] = flow_data[index-1]

        """Filter noise data"""
        filter_data = gaussian_filter1d(flow_data, sigma)

        exceedance_data = None
        for index, data in enumerate(filter_data):
            if data >= summer_baseflow:
                exceedance_data = data
                start_dates.append(index)
                current_fall_flush_block = filter_data[index: index + 5]
                fall_flush_duration.append(None)
                for current_flush_index, current_flush in enumerate(current_fall_flush_block):
                    if current_flush < summer_baseflow:
                        fall_flush_duration[-1] = current_flush_index + 1
                        break;
                break

        plt.figure()
        plt.plot(x_axis, flow_data, '.')
        plt.text(2, 2, 'summer: {}, actual: {}'.format(summer_baseflow, exceedance_data))
        plt.plot(x_axis, filter_data)
        plt.yscale('log')
        plt.axvline(x = start_dates[-1], color='brown')
        plt.axvline(x = start_of_summer[column_number], color = 'red')
        plt.savefig('post_processedFiles/Boxplots/{}.png'.format(column_number))

    return start_dates, fall_flush_duration

def calc_fall_return_to_wet(flow_matrix):
    sigma = 10
    return_dates = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Filter noise data"""
        filter_data = gaussian_filter1d(flow_data, sigma)

        for index, data in enumerate(filter_data):
            if index == len(filter_data) - 7:
                return_dates.append(None)
            elif (filter_data[index] - filter_data[index + 1]) / filter_data[index] > 0.5 and (filter_data[index + 1] - filter_data[index + 2]) / filter_data[index + 1] > 0.5 and (filter_data[index + 2] - filter_data[index + 3]) / filter_data[index + 2] > 0.5 and (filter_data[index + 3] - filter_data[index + 4]) / filter_data[index + 3] > 0.5 and (filter_data[index + 4] - filter_data[index + 5]) / filter_data[index + 4] > 0.5 and (filter_data[index + 5] - filter_data[index + 6]) / filter_data[index + 5] > 0.5 and (filter_data[index + 6] - filter_data[index + 7]) / filter_data[index + 6] > 0.5:
                return_dates.append(index)
                break;
    return return_dates
