import sys
import os
import glob
import errno
from datetime import date, datetime, timedelta
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array
import pandas as pd
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from pre_processFiles.gauge_reference import gauge_reference

def set_user_params(user_params, def_params):
    for key in def_params.keys():
        if key in user_params.keys():
            def_params[key] = user_params[key]

    return def_params

def calculate_average_each_column(matrix):
    average = []

    index = 0
    for _ in matrix[0]:
        average.append(np.nanmean(matrix[:, index]))
        index = index + 1

    return average


def create_folders():
    folders = ['post_processedFiles/Boxplots', 'post_processedFiles/Wateryear_Type', 'post_processedFiles/Class-1', 'post_processedFiles/Class-2', 'post_processedFiles/Class-3', 'post_processedFiles/Class-4', 'post_processedFiles/Class-5', 'post_processedFiles/Class-6', 'post_processedFiles/Class-7', 'post_processedFiles/Class-8', 'post_processedFiles/Class-9']

    for folder in folders:
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def median_of_time(lt):
    n = len(lt)
    if n < 1:
        return None
    elif n % 2 ==  1:
        return lt[n//2].start_date
    elif n == 2:
        first_date = lt[0].start_date
        second_date = lt[1].start_date
        return (first_date + second_date) / 2
    else:
        first_date = lt[n//2 - 1].start_date
        second_date = lt[n//2 + 1].start_date
        return (first_date + second_date) / 2

def median_of_magnitude(object_array):
    flow_array = []
    for obj in object_array:
        flow_array= flow_array + obj.flow

    return np.nanmean(np.array(flow_array, dtype=np.float))

def peak_magnitude(object_array):
    flow_array = []
    for obj in object_array:
        flow_array= flow_array + obj.flow
    
    return np.nanmax(np.array(flow_array, dtype=np.float))

def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html
    """
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1). Parameter: d for date object,
    years for added or subtracted years

    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def replace_nan(flow_data):
    for index, flow in enumerate(flow_data):
        if index == 0 and np.isnan(flow):
            flow_data[index] = 0
        elif np.isnan(flow):
            flow_data[index] = flow_data[index-1]
    return flow_data

def is_multiple_date_data(df):
    two_digit_year = '/' in df.iloc[4,0]
    year_in_front = '-' in df.iloc[4,0]

    if two_digit_year and len(str(df.iloc[4,0]).split("/")) > 1:
        return 2
    elif year_in_front and len(str(df.iloc[4,0]).split("-")) > 1:
        return 2
    else:
        print("return 1")
        return 1


def is_two_digit_year(date):
    return '/' in date[-3:]

def year_in_front(date):
    return '-' in date[-3:]


def get_date_from_offset_julian_date(row_number, year, start_date):
    start_year = year
    end_year = year + 1
    julian_start_date_start_year = datetime.strptime("{}/{}".format(start_date, start_year), "%m/%d/%Y").timetuple().tm_yday

    if start_year % 4 == 0:
        days_in_year_start = 366
    else:
        days_in_year_start = 365

    if row_number <= days_in_year_start - julian_start_date_start_year:
        current_year = start_year
        date_delta = julian_start_date_start_year + row_number
        current_date = datetime(current_year, 1, 1) + timedelta(date_delta - 1)
    else:
        current_year = end_year
        date_delta = row_number - days_in_year_start + julian_start_date_start_year - 1
        current_date = datetime(current_year, 1, 1) + timedelta(date_delta)

    return current_date

def moving_average(data_array):
    result_data = []
    for index, data in enumerate(data_array):
        if index < 2:
            result_data.append(data)
        elif index > len(data_array) - 3:
            result_data.append(data)
        else:
            result_data.append((data + data_array[index - 1] + data_array[index - 2] + data_array[index + 1] + data_array[index + 2])/5)
    return result_data


def get_nan_fraction_in_array(data_array):
    length_array = len(data_array)
    counter = 0
    for data in data_array:
        if pd.isnull(data):
            counter = counter + 1
    return counter / length_array

class Metric:

    def __init__(self, name):
        self.name = name
        self.data = []

    def add_class(self):
        self.data.append([])

    def insert_data(self, new_data):
        self.data[-1].append(new_data)

def crossings_nonzero_all(data):
    non_zero_array = []
    for index, element in enumerate(data):
        if index == len(data) - 5:
            return non_zero_array
        elif data[index + 1] > 0 and element < 0 :
            non_zero_array.append(index)
        elif data[index + 1] < 0 and element > 0 :
            non_zero_array.append(index)


def find_index(arr, item):
    for index, element in enumerate(arr):
        if element == item:
            return index

def nonP_box_plot(dictionary):
    boxplot_code = ['SM', 'HSR', 'LSR', 'WS', 'GW', 'PGR', 'FER', 'RSG', 'HLP']
    boxplot_color = ['#FFEB3B', '#0D47A1','#80DEEA','#FF9800','#F44336','#8BC34A','#F48FB1','#7E57C2','#C51162', '#212121']
    none_log = ['Feq', 'Tim', 'NoFlow']

    for key in dictionary:
        for index, class_array in enumerate(dictionary[key]):
            dictionary[key][index] = [ele for ele in class_array if not np.isnan(ele)]

    # for key in dictionary:
    #     plt.ion()
    #     plt.figure(key)
    #     plt.title(key)
    #     box = plt.boxplot(dictionary[key], patch_artist=True, showfliers=False)
    #     plt.xticks([1,2,3,4,5,6,7,8,9], boxplot_code)
    #     plt.tick_params(labelsize=6)
    #     # plt.yscale('log')
    #     if any(x in key for x in none_log):
    #         plt.yscale('linear')
    #     for patch, color in zip(box['boxes'], boxplot_color):
    #         patch.set_facecolor(color)
    #     plt.savefig('post_processedFiles/Boxplots/{}.png'.format(key))

def smart_plot(result_matrix):
    boxplot_code = ['SM', 'HSR', 'LSR', 'WS', 'GW', 'PGR', 'FER', 'RSG', 'HLP']
    boxplot_color = ['#FFEB3B', '#0D47A1','#80DEEA','#FF9800','#F44336','#8BC34A','#F48FB1','#7E57C2','#C51162', '#212121']
    none_log = ['Feq', 'Tim', 'NoFlow']

    metrics = []
    for row in result_matrix:
        metrics.append(row[0])

    result = {}
    for metric in metrics:
        result[metric] = []
        result[metric].append([])

    for column_number, class_number in enumerate(result_matrix[0]):

        if column_number == 0:
            continue

        """Append Data to the last array"""
        for row_number, metric in enumerate(metrics):
            if bool(result_matrix[row_number][column_number] and not np.isnan(result_matrix[row_number][column_number])) or result_matrix[row_number][column_number] == 0:
                result[metric][-1].append(result_matrix[row_number][column_number])

        # """Plot at the last column"""
        # if column_number == len(result_matrix[0]) - 1:
        #     plt.ion()

        #     for row_number, metric in enumerate(metrics):
        #         """Ignore plots for class number and gauge number"""
        #         if row_number > 1:
        #             plt.figure(metric)
        #             plt.title(metric)
        #             box = plt.boxplot(result[metric], patch_artist=True, showfliers=False)
        #             plt.xticks([1,2,3,4,5,6,7,8,9], boxplot_code)
        #             plt.tick_params(labelsize=6)
        #             # plt.yscale('log')
        #             if any(x in metric for x in none_log):
        #                 plt.yscale('linear')
        #             for patch, color in zip(box['boxes'], boxplot_color):
        #                 patch.set_facecolor(color)
        #             plt.savefig('post_processedFiles/Boxplots/{}.png'.format(metric))

        # elif result_matrix[0][column_number + 1] != result_matrix[0][column_number]:
        #     """Append an empty array if changing class number"""
        #     for metric in metrics:
        #         result[metric].append([])

def remove_offset_from_julian_date(julian_offset_date, julian_start_date):
    """offset date counts 0 for start date. Converted to use 0 for 1/1"""
    if bool(not julian_offset_date or np.isnan(julian_offset_date)) and julian_offset_date != 0:
        julian_nonoffset_date = np.nan
    elif julian_offset_date < 366 - julian_start_date:
        julian_nonoffset_date = julian_offset_date + julian_start_date
    else:
        julian_nonoffset_date = julian_offset_date - (365 - julian_start_date)
    return julian_nonoffset_date


def get_calculation_numbers():

    from utils.upload_files import upload_files

    directory_name = 'rawFiles'
    input_files = 'user_input_files'
    selected_files = []

    calculation_number = None
    while not calculation_number:
        print('')
        print('Select the Following Calculations:')
        calculation_number = int(input(' 1. Winter High Flow\n 2. Spring Transition\n 3. Summer Baseflow\n 4. Fall Flush \n 5. Fall Winter Baseflow \n 6. All Year \n 7. Create Annual Flow Matrix CSV \n 8. Winter High Flow POR \n 9. Upload Files \n \tEnter your choice => '))

    if calculation_number > 9:
        print('')
        print('What did you just do?')
        os._exit(0)

    if calculation_number == 9:
        csv_files = glob.glob1(input_files, '*.csv')
        pick_all = True

        while csv_files:
            file_selection = "\nPick file to upload\n"
            if pick_all:
                file_selection = file_selection + ' 0. Upload All Files\n'
            for i, file in enumerate(csv_files):
                file_selection = file_selection + ' ' + str(i+1) + '. ' + file + '\n'
            file_selection = file_selection + '\t' + 'Enter your choice => '
            selection = int(input(file_selection))
            if selection == 0:
                for i, file in enumerate(csv_files):
                    selected_files.append(input_files + '/' + file)
                break

            selected_files.append(input_files + '/' + csv_files[selection - 1])
            csv_files.remove(csv_files[selection -1])
            if not csv_files:
                break
            pick_next = int(input('\nWould you like to upload more files? \n 1. YES\n 2. NO\nEnter your choice => '))
            if pick_next == 1:
                pick_all= False
                continue
            else:
                break
        
        flow_class = int(input('Select the natural flow class matching your data. Default: 3 => '))
        if not flow_class:
            flow_class = int(3)
        if flow_class > 9:
            print('')
            print('Please select a flow class numbered 1-9')
            os._exit(0)

    start_date = input('Start Date of each water year? Default: 10/1 => ')
    if not start_date:
        start_date = '10/1'

    if calculation_number == 9:
        print('Uploading files with start date: {} in {} directory'.format(start_date, directory_name))
        upload_files(start_date, selected_files, flow_class)
        return calculation_number, start_date, flow_class, None 

    gauge_or_class = int(input('Input 1 to calculate entire Class, 2 for Gauge(s), or 3 for All Gauges=> '))
    if gauge_or_class == 1:
        gauge_numbers = None
        class_number = input('Class Number? Default: 3 => ')
        if not class_number:
            class_number = 3
        class_number = int(class_number)
    elif gauge_or_class == 2:
        class_number = None
        gauge_numbers = input('Gauge Number(s)? Seprated , Default: 11237500 => ')
        if not gauge_numbers:
            gauge_numbers = '11237500'
        gauge_numbers = [int(x.strip()) for x in gauge_numbers.split(',')]
        for gauge_number in gauge_numbers:
            if int(gauge_number) not in gauge_reference:
                print('')
                print('What did you just do?')
                os._exit(0)
    elif gauge_or_class == 3:
        class_number = None
        gauge_numbers = None
    else:
        print('')
        print('Something went wrong there!')
        os._exit(0)

    return calculation_number, start_date, class_number, gauge_numbers


def create_wateryear_labels(result_matrix):
    wateryear_type_matrix = [None] * 5
    wateryear_type_list = []
    ''' extract average daily flow values from results matrix'''
    avg_daily_flow = result_matrix[1]
    perc_3333 = np.nanpercentile(avg_daily_flow, 33.33)
    perc_6666 = np.nanpercentile(avg_daily_flow, 66.66)
    perc_100 = np.nanmax(avg_daily_flow)
    for index, flow_val in enumerate(avg_daily_flow):
        if flow_val < perc_3333:
            wateryear_type = 'DRY'
        elif flow_val < perc_6666:
            wateryear_type = 'MODERATE'
        elif flow_val <= perc_100:
            wateryear_type = 'WET'
        else:
            wateryear_type = NaN
        wateryear_type_list.append(wateryear_type)

    flow_years = result_matrix[0]
    wateryear_type_matrix[0] = ['year'] + flow_years
    wateryear_type_matrix[1] = ['WYT'] + wateryear_type_list
    wateryear_type_matrix[2] = ['mean_ann_Q'] + avg_daily_flow
    wateryear_type_matrix[3] = ['perc_33.33'] + [perc_3333]*len(flow_years)
    wateryear_type_matrix[4] = ['perc_66.66'] + [perc_6666]*len(flow_years)


    wateryear_type_matrix = list(map(list, zip(*wateryear_type_matrix)))

    return wateryear_type_matrix

