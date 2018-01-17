import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt

from datetime import date, datetime
from xlrd import open_workbook, xldate_as_tuple



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


def import_and_parse_csv(path):
    """Return 3 arrays for year, julian_date, and flow, and calculate
    number of years given in each dataset. Parameter: path for csv file path

    """
    year = []
    julian_date = []
    flow = []
    number_of_years = 0
    flow_index = 0

    with open(path) as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        current_year = 0

        for row in file:
            if row[0] == 'Date':
                for column in row:
                    if 'Flow' in column:
                        break
                    flow_index = flow_index + 1
                continue
            current_date = datetime.strptime(row[0], "%m/%d/%y")
            """reduce by 100 when '88' is interprated as 2088"""
            if current_date.year > 2017:
                current_date = add_years(current_date, -100)
            year.append(current_date.year)
            julian_date.append(current_date.timetuple().tm_yday)

            if row[flow_index] == "" or row[flow_index] == "NA":
                flow.append(None)
            else:
                flow.append(row[flow_index])

            if current_date.year != current_year:
                current_year = current_date.year
                number_of_years = number_of_years + 1
    return year, julian_date, flow, number_of_years

def import_and_parse_xlsm(path):
    """Return 3 arrays for year, julian_date, and flow, and calculate
    number of years given in each dataset. Parameter: path for csv file path

    """
    year = []
    julian_date = []
    flow = []
    flow_index = 0
    number_of_years = 0
    current_year = 0

    book = open_workbook(path)
    sheet = book.sheet_by_index(1)

    for column in sheet.row(0):
        if 'Flow' in column.value:
            break
        flow_index = flow_index + 1

    for row in range(1, sheet.nrows):

        parsed_year, parsed_month, parsed_day, hour, minute, second = xldate_as_tuple(sheet.cell(row,0).value, book.datemode)
        dt = datetime(year=parsed_year, month=parsed_month, day=parsed_day)

        year.append(parsed_year)
        julian_date.append(dt.timetuple().tm_yday)

        if sheet.cell(row, flow_index).value == "" or sheet.cell(row, flow_index).value == "NA":
            flow.append(None)
        else:
            flow.append(sheet.cell(row, flow_index).value)


        if parsed_year != current_year:
            current_year = parsed_year
            number_of_years = number_of_years + 1
    return year, julian_date, flow, number_of_years

def get_offset_julian_date(julian_date, julian_start_date, days_in_year):
    return julian_date - start_julian_date + days_in_year

def get_year_ranges_from_julian_dates(julian_dates, years, start_date):
    julian_start_date_first_year = datetime.strptime("{}/{}".format(start_date, years[0]), "%m/%d/%Y").timetuple().tm_yday
    julian_start_date_last_year = datetime.strptime("{}/{}".format(start_date, years[-1]), "%m/%d/%Y").timetuple().tm_yday

    if (julian_dates[0] < julian_start_date_first_year):
        first_year = years[0] - 1
    else:
        first_year = years[0]

    if(julian_dates[-1] >= julian_start_date_last_year):
        last_year = years[-1] + 1
    else:
        last_year = years[-1]

    year_ranges = list(range(first_year, last_year))
    return year_ranges

def get_position(year, julian_date, year_ranges, julian_start_date, days_in_year):
    row = julian_date - julian_start_date
    if (row < 0):
        row = row + days_in_year

    if(year > year_ranges[-1]):
        column = -1
    else:
        column = year_ranges.index(year)
        if (julian_date < julian_start_date):
            column = column - 1

    return row, column

def get_flow_matrix(years, julian_dates, flow, year_ranges, start_date):
    """Return one matrix containing flow data for raw dataset based on start date
    """

    number_of_columns = len(year_ranges)

    flow_matrix = np.zeros((366, number_of_columns))
    flow_matrix.fill(None)

    for index, julian_date in enumerate(julian_dates):
        if (years[index] % 4 == 0):
            days_in_year = 366
        else:
            days_in_year = 365

        julian_start_date = datetime.strptime("{}/{}".format(start_date, years[index]), "%m/%d/%Y").timetuple().tm_yday
        row, column = get_position(years[index], julian_date, year_ranges, julian_start_date, days_in_year)

        flow_matrix[row][column] = flow[index]

    return flow_matrix

def convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date):
    """Summary Function
    """

    current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column = extract_current_data_at_index(fixed_df, current_gaguge_column_index)
    date_column, flow_column = remove_nan_from_date_and_flow_columns(raw_date_column, raw_flow_column)
    years, julian_dates, number_of_years = extract_info_from_date(date_column)
    year_ranges = get_year_ranges_from_julian_dates(julian_dates, years, start_date)

    flow_matrix = get_flow_matrix(years, julian_dates, flow_column, year_ranges, start_date)
    return current_gauge_class, current_gauge_number, year_ranges, flow_matrix



def calculate_matrix_percentile(matrix):
    ten_percentile_array = []
    fifty_percentile_array = []
    ninty_percentile_array = []

    index = 0
    for flow in matrix[0]:
        ten_percentile_array.append(np.nanpercentile(matrix[:, index], 10))
        fifty_percentile_array.append(np.nanpercentile(matrix[:, index], 50))
        ninty_percentile_array.append(np.nanpercentile(matrix[:, index], 90))
        index = index + 1
    return ten_percentile_array, fifty_percentile_array, ninty_percentile_array

def calculate_average_each_column(matrix):
    average = []

    index=0
    for flow in matrix[0]:
        average.append(np.nanmean(matrix[:,index]))
        index = index + 1

    return average

def calculate_std_each_column(matrix):
    std = []

    index=0
    for flow in matrix[0]:
        std.append(np.nanstd(matrix[:,index]))
        index = index + 1

    return std

def calculate_cov_each_column(std_array, average_array):
    cov = []

    index=0
    for average in average_array:
        cov.append(std_array[index] / average)
        index = index + 1
    return cov

def calculate_percent_exceedance(matrix, percentile):
    return np.nanpercentile(matrix, percentile)

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

def remove_nan_from_date_and_flow_columns(raw_date, raw_flow):
    """Loop through the date and remove all date with NA values.
    The purpose is to clean the data before creating the final matrix.
    """
    date_column = []
    flow_column = []


    index = 0
    for data in raw_date:
        if not pd.isnull(data) and index > 1:
            date_column.append(raw_date[index])
            flow_column.append(raw_flow[index])
        index = index + 1
    return date_column, flow_column

def extract_info_from_date(date):
    years=[]
    julian_date=[]
    number_of_years=0

    current_year = 0
    for single_date in date:
        if is_two_digit_year(single_date):
            dt = datetime.strptime(single_date, "%m/%d/%y")
        else:
            dt = datetime.strptime(single_date, "%m/%d/%Y")

        if dt.year > 2019:
            parsed_year = dt.year - 100
        else:
            parsed_year = dt.year
        years.append(parsed_year)
        julian_date.append(dt.timetuple().tm_yday)

        if parsed_year != current_year:
            current_year = parsed_year;
            number_of_years = number_of_years + 1

    return years, julian_date, number_of_years

def extract_current_data_at_index(fixed_df, current_gaguge_column_index):
    current_gauge_number = fixed_df.iloc[1, current_gaguge_column_index]
    current_gauge_class = fixed_df.iloc[0, current_gaguge_column_index]

    if is_multiple_date_data(fixed_df):
        raw_date_column = fixed_df.iloc[:, current_gaguge_column_index - 1]
    else:
        raw_date_column = fixed_df.iloc[:, 0]
    raw_flow_column = fixed_df.iloc[:, current_gaguge_column_index]

    return current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column

def sort_matrix(matrix, index):
    row = len(matrix)
    column = len(matrix[0])
    index_array = np.argsort(matrix[index])
    sorted_matrix = np.zeros((row, column))

    counter = 0
    for index in index_array:
        sorted_matrix[:,counter] = matrix[:,index]
        counter = counter + 1

    return sorted_matrix

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
            plt.savefig('processedFiles/{}.png'.format(metrics[13]))

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
