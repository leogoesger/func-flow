import numpy as np
import matplotlib.pyplot as plt
from helpers import moving_average

def start_of_summer(matrix, start_date):
    start_of_summer = []

    for index, flow in enumerate(matrix[0]):
        twenty_percentile = np.nanpercentile(matrix[:, index], 20)
        smooth_data = moving_average(matrix[:,index])

        for data_index, data in enumerate(smooth_data):
            if (data_index >= len(smooth_data) - 2):
                break
            elif data < twenty_percentile and smooth_data[data_index+1] < twenty_percentile and smooth_data[data_index+2] < twenty_percentile:
                start_of_summer.append(data_index)
                break

        plt.figure(index)
        plt.plot(matrix[:, index], '-')
        plt.title('Start of Summer Metric')
        plt.text(250, max(matrix[:,index])-100, 'Start of Summer: {}'.format(start_of_summer[index]))
        plt.xlabel('Julian Day')
        plt.ylabel('Flow, ft^3/s')
        plt.axvline(start_of_summer[index], color='red')
        plt.axhline(twenty_percentile)
        plt.savefig('processedFiles/StartSummer/{}.png'.format(index+1))

    return start_of_summer
