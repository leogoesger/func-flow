import numpy as np
from utils.helpers import moving_average, get_nan_fraction_in_array


def calc_start_of_summer(matrix, start_date):

    start_dates = []

    for index, flow in enumerate(matrix[0]):
        twenty_percentile = np.nanpercentile(matrix[:, index], 20)
        smooth_data = moving_average(matrix[:, index])

        for data_index, data in enumerate(smooth_data):

            if (data_index >= len(smooth_data) - 6):
                start_dates.append(float('NaN'))
                break
            elif data_index > 75 and data <= twenty_percentile and smooth_data[data_index + 1] <= twenty_percentile and \
                smooth_data[data_index + 2] <= twenty_percentile and smooth_data[data_index + 3] <= twenty_percentile and smooth_data[data_index + 4] <= twenty_percentile:
                start_dates.append(data_index)
                break

        # if get_nan_fraction_in_array(matrix[:, index]) > 0.2:
        #     continue
        # else:
        #     plt.figure(index)
        #     plt.plot(matrix[:, index], '-')
        #     plt.title('Start of Summer Metric')
        #     plt.text(1, max(matrix[:,index])-100, 'Start of Summer: {}'.format(start_dates[index]))
        #     plt.xlabel('Julian Day')
        #     plt.ylabel('Flow, ft^3/s')
        #     plt.axvline(start_dates[index], color='red')
        #     plt.axhline(twenty_percentile)
        #     plt.savefig('processedFiles/StartSummer/{}.png'.format(index+1))

    return np.nanpercentile(start_dates, 10), np.nanpercentile(start_dates, 50), np.nanpercentile(start_dates, 90)
