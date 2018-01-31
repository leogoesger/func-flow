import numpy as np
import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix, insert_column_header
from utils.calc_spring_transition import calc_spring_transition_timing

np.warnings.filterwarnings('ignore')

def spring_transition():
    start_date = '10/1'
    directoryName = 'rawFiles'
    endWith = '.csv'

    for root,dirs,files in os.walk(directoryName):
        for file in files:
           if file.endswith(endWith):

               fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
               step = is_multiple_date_data(fixed_df);

               current_gaguge_column_index = 1
               while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                   if fixed_df.iloc[1,current_gaguge_column_index] == 11419000:
                       current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                       calc_spring_transition_timing(flow_matrix)


                   current_gaguge_column_index = current_gaguge_column_index + step
