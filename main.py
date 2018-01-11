import numpy as np

from helpers import convert_raw_data_to_matrix
import os


for root,dirs,files in os.walk('rawFiles'):
    for file in files:
       if file.endswith(".xlsm"):
           flow_matrix = convert_raw_data_to_matrix('rawFiles/{}'.format(file))
           print(flow_matrix)
           np.savetxt("processedFiles/{}.csv".format(file), flow_matrix, delimiter=",")
