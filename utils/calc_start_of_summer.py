import numpy as np
import matplotlib.pyplot as plt
from utils.helpers import moving_average, get_nan_fraction_in_array


def calc_start_of_summer(matrix, start_date):

    start_dates = []
    failed_calcs = 0

    for index, flow in enumerate(matrix[0]):
        # calculate the percentile which gives the 73 lowest flow days in the second half of the water year
        percentile = np.nanpercentile(matrix[182:len(matrix[:]-1)], 40)
        
        smooth_data = moving_average(matrix[:, index])
        search_range = smooth_data.index(max(smooth_data))

        for data_index, data in enumerate(smooth_data):
            
            # For a low flow percentile = 0, only require smoothed flow to stay at Q=0 for three days
            if percentile == 0:
                if (data_index > len(smooth_data) - 3):
                    start_dates.append(float('NaN'))
                    break
                elif data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile:
                    start_dates.append(data_index)
            # When the low flow percentile is above zero, require smoothed flow to stay under threshold for four days
            else:
                if (data_index > len(smooth_data) - 4):
                    start_dates.append(float('NaN'))
                    break
                if data_index >= search_range and data <= percentile and smooth_data[data_index + 1] <= percentile and \
                smooth_data[data_index + 2] <= percentile and smooth_data[data_index + 3] <= percentile:
                    start_dates.append(data_index)
                    break

        if start_dates[index] == search_range:
            start_dates[index] == np.nan
        elif start_dates[index] == 0:
            start_dates[index] == np.nan
        elif np.isnan(start_dates[index]) == True:
            failed_calcs = failed_calcs + 1
        
#        plt.figure(index)
#        plt.plot(matrix[:, index], '-')
#        plt.plot(smooth_data)
#        plt.title('Start of Summer Metric')
#        plt.xlabel('Julian Day')
#        plt.ylabel('Flow, ft^3/s')
#        plt.axvline(start_dates[index], color='red')
#        plt.axhline(percentile)
#        plt.axvline(search_range)
#        plt.savefig('post_processedFiles/StartSummer/{}.png'.format(index+1))
            
    
#    for index, dates in enumerate(start_dates):
#        if start_dates[index] == search_range:
#            start_dates[index] == np.nan
#            failed_calcs = failed_calcs + 1
#        elif start_dates[index] == 0:
#            start_dates[index] == np.nan
#            failed_calcs = failed_calcs + 1
    print(start_dates)
    print('Test failed for {} out of {} water years.'.format(failed_calcs, matrix.shape[1]))

    
    return start_dates
