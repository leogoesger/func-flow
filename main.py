import numpy as np

from helpers import convert_raw_data_to_matrix, calculate_matrix_percentile, calculate_average_each_column
import os

np.warnings.filterwarnings('ignore')

for root,dirs,files in os.walk('rawFiles'):
    for file in files:
       if file.endswith(".xlsm"):
           print('Processing {}...'.format(file))
           flow_matrix = convert_raw_data_to_matrix('rawFiles/{}'.format(file))

           average_each_year = calculate_average_each_column(flow_matrix)
           ten, fifty, ninty = calculate_matrix_percentile(flow_matrix)

           average_of_average = np.nanmean(average_each_year)
           average_ten = np.nanmean(ten)
           average_fifty = np.nanmean(fifty)
           average_ninty = np.nanmean(ninty)

           print('Average of average flow each year: {}'.format(round(average_of_average,2)))
           print('Average of 10th percentile: {}'.format(round(average_ten,2)))
           print('Average of 50th percentile: {}'.format(round(average_fifty,2)))
           print('Average of 90th percentile: {}\n'.format(round(average_ninty,2)))

           # flow_matrix = np.vstack((flow_matrix, np.full(len(ten), -999)))
           # flow_matrix = np.vstack((flow_matrix, np.array(average_each_year)))
           # flow_matrix = np.vstack((flow_matrix, np.array(ten)))
           # flow_matrix = np.vstack((flow_matrix, np.array(fifty)))
           # flow_matrix = np.vstack((flow_matrix, np.array(ninty)))


           f = open('processedFiles/result_{}.txt'.format(file),'w')
           f.write('Average of average flow each year: {}\n'.format(average_of_average))
           f.write('Average of 10th percentile: {}\n'.format(average_ten))
           f.write('Average of 50th percentile: {}\n'.format(average_fifty))
           f.write('Average of 90th percentile: {}\n'.format(average_ninty))
           f.close()

           # np.savetxt("processedFiles/{}.csv".format(file), flow_matrix, delimiter=",")
