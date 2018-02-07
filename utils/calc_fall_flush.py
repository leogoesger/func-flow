import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def calc_fall_flush_timing_duration(flow_matrix, start_of_summer):
    sigma = 10
    start_dates = []
    fall_flush_duration = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        """Summer baseflow determined by the previous year if not the first year"""
        if column_number == 0:
            print(start_of_summer)
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[ start_of_summer[0] : 361, 0 ])
        elif start_of_summer[column_number - 1] and 361 > start_of_summer[column_number - 1]:
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[start_of_summer[column_number]:361, column_number - 1])
        elif start_of_summer[column_number] > 366:
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[start_of_summer[column_number] - 366 : start_of_summer[column_number] - 346, column_number])

        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Filter noise data"""
        filter_data = gaussian_filter1d(flow_data, sigma)

        for index, data in enumerate(filter_data):
            if data >= summer_baseflow:
                start_dates.append(index)
                current_fall_flush_block = filter_data[index, index + 5]
                fall_flush_duration.append(None)
                for current_flush_index, current_flush in current_fall_flush_block:
                    if current_flush < summer_baseflow:
                        fall_flush_duration[-1] = current_flush_index + 1
                        break;
                break

        plt.figure()
        plt.plot(x_axis, flow_data, '.')
        plt.plot(x_axis, filter_data)
        plt.axvline(x = start_dates[-1], color='green')
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
