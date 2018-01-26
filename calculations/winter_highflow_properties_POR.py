import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix
from utils.calc_winter_highflow_properties import calculate_timing_duration_frequency_POR, GaugeInfo

np.warnings.filterwarnings('ignore')


def timing_duration_frequency_POR(start_date, directoryName, endWith, class_number, gauge_number):
    exceedance_percent = [2, 5, 10, 20, 50]
    timing = {}
    duration = {}

    gauges = []

    for i in exceedance_percent:
        timing[i] = []
    for root,dirs,files in os.walk(directoryName):
        for file in files:
           if file.endswith(endWith):

               fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
               step = is_multiple_date_data(fixed_df);

               current_gaguge_column_index = 1

               while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                   if gauge_number:
                       if int(fixed_df.iloc[1, current_gaguge_column_index]) == int(gauge_number):
                           current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                           current_timing, current_duration, current_freq, current_magnitude = calculate_timing_duration_frequency_POR(flow_matrix, year_ranges, start_date, exceedance_percent)

                           gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                           break;
                   elif int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                       current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                       current_timing, current_duration, current_freq, current_magnitude = calculate_timing_duration_frequency_POR(flow_matrix, year_ranges, start_date, exceedance_percent)

                       gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                   current_gaguge_column_index = current_gaguge_column_index + step


    for gauge in gauges:
        gauge.plot_based_on_exceedance()
        gauge.plot_timing()
        gauge.plot_duration()
        gauge.plot_mag()
