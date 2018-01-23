import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix, sort_matrix
from utils.calc_winter_highflow_properties import calculate_timing_duration_frequency_single_gauge

np.warnings.filterwarnings('ignore')

class GaugeInfo:

    def __init__(self, class_number, gauge_number, timing, duration, freq, mag, exceedance_percent):
        self.class_number = class_number
        self.gauge_number = gauge_number
        self.timing = timing
        self.duration = duration
        self.freq = freq
        self.mag = mag
        self.exceedance_percent = exceedance_percent

    def plot_timing(self):
        plt.figure('Timing - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))
        timing_array = []
        for percent in self.exceedance_percent:
            timing_array.append(self.timing[percent])
        plt.boxplot(timing_array)
        plt.xticks( range(6), ('', '2%', '5%', '10%', '20%', '50%') )
        plt.savefig('post_processedFiles/Boxplots/{}_timing.png'.format(self.gauge_number))

    def plot_duration(self):
        plt.figure('Duration - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))
        duration_array=[]
        for percent in self.exceedance_percent:
            duration_array.append(self.duration[percent])
        plt.boxplot(duration_array)
        plt.xticks( range(6), ('', '2%', '5%', '10%', '20%', '50%') )
        plt.savefig('post_processedFiles/Boxplots/{}_duration.png'.format(self.gauge_number))

    def plot_mag(self):
        plt.figure('Freq - Class: {}, Gauge Number: {}'.format(self.class_number, self.gauge_number))
        mag_array = []
        for percent in self.exceedance_percent:
            mag_array.append(self.mag[percent])
        plt.boxplot(mag_array)
        plt.xticks( range(6), ('', '2%', '5%', '10%', '20%', '50%') )
        plt.savefig('post_processedFiles/Boxplots/{}_mag.png'.format(self.gauge_number))

    def plot_based_on_exceedance(self):
        for percent in self.exceedance_percent:
            plt.figure('Class: {}, Gauge Number: {}, {}%'.format(self.class_number, self.gauge_number, percent), figsize=(5,5))
            plt.subplot(131)
            plt.boxplot(self.timing[percent])
            plt.gca().set_title('Timing')
            plt.subplot(132)
            plt.boxplot(self.duration[percent])
            plt.gca().set_title('Duration')
            plt.subplot(133)
            plt.boxplot(self.mag[percent])
            plt.gca().set_title('Magnitude')
            plt.tight_layout()
            plt.savefig('post_processedFiles/Boxplots/{}_{}.png'.format(int(self.gauge_number), percent))



def timing_duration_frequency_singular(start_date, directoryName, endWith, class_number, gauge_number):
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

               if is_multiple_date_data(fixed_df):
                   print('Current Datset uses one date per column of data')
                   step = 2
               else:
                   print('Current Datset uses the same date per column of data')
                   step = 1

               current_gaguge_column_index = 1

               while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                   if gauge_number:
                       if int(fixed_df.iloc[1, current_gaguge_column_index]) == int(gauge_number):
                           current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                           current_timing, current_duration, current_freq, current_magnitude = calculate_timing_duration_frequency_single_gauge(flow_matrix, year_ranges, start_date, exceedance_percent)

                           gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                           break;
                   elif int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                       current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                       current_timing, current_duration, current_freq, current_magnitude = calculate_timing_duration_frequency_single_gauge(flow_matrix, year_ranges, start_date, exceedance_percent)

                       gauges.append(GaugeInfo(current_gauge_class, current_gauge_number, current_timing, current_duration, current_freq, current_magnitude, exceedance_percent))

                   current_gaguge_column_index = current_gaguge_column_index + step


    for gauge in gauges:
        gauge.plot_based_on_exceedance()
