import matplotlib.pyplot as plt
import pandas as pd

from datetime import date, datetime


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



def is_multiple_date_data(df):
    two_digit_year = '/' in df.iloc[4,0][-4:]
    try:
        if two_digit_year:
            datetime.strptime(df.iloc[4,0], "%m/%d/%y")
            datetime.strptime(df.iloc[4,2], "%m/%d/%y")
            datetime.strptime(df.iloc[4,4], "%m/%d/%y")
        else:
            datetime.strptime(df.iloc[4,0], "%m/%d/%Y")
            datetime.strptime(df.iloc[4,2], "%m/%d/%Y")
            datetime.strptime(df.iloc[4,4], "%m/%d/%Y")
        return True

    except Exception as e:
        return False

def is_two_digit_year(date):
    if '/' in date[-3:]:
        return True
    else:
        return False


def get_date_from_offset_julian_date(row_number, year, start_date):
    start_year = year
    end_year = year + 1
    julian_start_date_start_year = datetime.strptime("{}/{}".format(start_date, start_year), "%m/%d/%Y").timetuple().tm_yday
    julian_start_date_end_year = datetime.strptime("{}/{}".format(start_date, end_year), "%m/%d/%Y").timetuple().tm_yday

    if start_year % 4 == 0:
        start_days_in_year = 366
    else:
        start_days_in_year = 365

    if end_year % 4 == 0:
        end_days_in_year = 366
    else:
        end_days_in_year = 365

    if start_days_in_year == 365 and end_days_in_year == 365:
        if row_number <= start_days_in_year - julian_start_date_start_year:
            current_year = start_year
            current_julian_date = datetime.datetime(current_year, 1, 1) + datetime.timedelta(julian_start_date_start_year + row_number)
        else:
            current_year = end_year
            current_julian_date = datetime.datetime(current_year, 1, 1) + datetime.timedelta(row_number - start_days_in_year + julian_start_date_start_year - 1)


def moving_average(data_array):
    result_data = []
    for index, data in enumerate(data_array):
        if index <= 3:
            result_data.append(data_array[index])
        else:
            result_data.append((data_array[index] + data_array[index - 1] + data_array[index - 2] + data_array[index - 3] + data_array[index - 4])/5)
    return result_data

def get_nan_fraction_in_array(data_array):
    length_array = len(data_array)
    counter = 0
    for data in data_array:
        if pd.isnull(data):
            counter = counter + 1
    return counter / length_array


def plot_matrix(result_matrix):

    metrics = ['Gauge_Class', 'Gauge_Number', 'Two_Percent_Exceedance', 'Five_Percent_Exceedance', 'Ten_Percent_Exceedance', 'Twenty_Percent_Exceedance', 'Fifty_Percent_Exceedance', 'Average_of_Average', 'Ten_Percentile_Average', 'Fifty_Percentile_Average', 'Ninty_Percentile_Average', 'Ten_Percentile_COV', 'Fifty_Percentile_COV', 'Ninty_Percentile_COV']

    current_class_index = 0

    two_percent_exceedance_array = []
    two_percent_exceedance_array.append([])

    five_percent_exceedance_array = []
    five_percent_exceedance_array.append([])

    ten_percent_exceedance_array = []
    ten_percent_exceedance_array.append([])

    twenty_percent_exceedance_array = []
    twenty_percent_exceedance_array.append([])

    fifty_percent_exceedance_array = []
    fifty_percent_exceedance_array.append([])

    average_average_array = []
    average_average_array.append([])

    ten_percentile_average_array = []
    ten_percentile_average_array.append([])

    fifty_percentile_average_array = []
    fifty_percentile_average_array.append([])

    ninty_percentile_average_array = []
    ninty_percentile_average_array.append([])

    ten_percentile_cov_array = []
    ten_percentile_cov_array.append([])

    fifty_percentile_cov_array = []
    fifty_percentile_cov_array.append([])

    ninty_percentile_cov_array = []
    ninty_percentile_cov_array.append([])

    for index, class_number in enumerate(result_matrix[0]):

        two_percent_exceedance_array[current_class_index].append(result_matrix[2, index])
        five_percent_exceedance_array[current_class_index].append(result_matrix[3, index])
        ten_percent_exceedance_array[current_class_index].append(result_matrix[4, index])
        twenty_percent_exceedance_array[current_class_index].append(result_matrix[5, index])
        fifty_percent_exceedance_array[current_class_index].append(result_matrix[6, index])
        average_average_array[current_class_index].append(result_matrix[7, index])
        ten_percentile_average_array[current_class_index].append(result_matrix[8, index])
        fifty_percentile_average_array[current_class_index].append(result_matrix[9, index])
        ninty_percentile_average_array[current_class_index].append(result_matrix[10, index])
        ten_percentile_cov_array[current_class_index].append(result_matrix[11, index])
        fifty_percentile_cov_array[current_class_index].append(result_matrix[12, index])
        ninty_percentile_cov_array[current_class_index].append(result_matrix[13, index])

        if index == len(result_matrix[0]) - 1:
            plt.figure(metrics[2])
            plt.boxplot(two_percent_exceedance_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[2]))
            plt.figure(metrics[3])
            plt.boxplot(five_percent_exceedance_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[3]))
            plt.figure(metrics[4])
            plt.boxplot(ten_percent_exceedance_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[4]))
            plt.figure(metrics[5])
            plt.boxplot(twenty_percent_exceedance_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[5]))
            plt.figure(metrics[6])
            plt.boxplot(fifty_percent_exceedance_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[6]))
            plt.figure(metrics[7])
            plt.boxplot(average_average_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[7]))
            plt.figure(metrics[8])
            plt.boxplot(ten_percentile_average_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[8]))
            plt.figure(metrics[9])
            plt.boxplot(fifty_percentile_average_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[9]))
            plt.figure(metrics[10])
            plt.boxplot(ninty_percentile_average_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[10]))
            plt.figure(metrics[11])
            plt.boxplot(ten_percentile_cov_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[11]))
            plt.figure(metrics[12])
            plt.boxplot(fifty_percentile_cov_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[12]))
            plt.figure(metrics[13])
            plt.boxplot(ninty_percentile_cov_array)
            plt.savefig('processedFiles/Boxplots/{}.png'.format(metrics[13]))

        elif result_matrix[0, index + 1] != class_number:
            current_class_index = current_class_index + 1

            two_percent_exceedance_array.append([])
            five_percent_exceedance_array.append([])
            ten_percent_exceedance_array.append([])
            twenty_percent_exceedance_array.append([])
            fifty_percent_exceedance_array.append([])
            average_average_array.append([])
            ten_percentile_average_array.append([])
            fifty_percentile_average_array.append([])
            ninty_percentile_average_array.append([])
            ten_percentile_cov_array.append([])
            fifty_percentile_cov_array.append([])
            ninty_percentile_cov_array.append([])
