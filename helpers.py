import numpy as np
import csv
import pandas as pd

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

def convert_raw_data_to_matrix(years, julian_dates, flow, number_of_years):
    """Return one matrix containing flow data for raw dataset

    """


    flow_matrix = np.zeros((366, number_of_years))
    flow_matrix.fill(None)
    current_column = 0
    current_flow_index = 0
    current_year = years[0]

    for index, year in enumerate(years):
        if year == current_year:
            flow_matrix[julian_dates[index] - 1][current_column] = flow[current_flow_index]
            current_flow_index = current_flow_index + 1
        elif year != current_year:
            current_column = current_column + 1
            current_year = year
            flow_matrix[julian_dates[index] - 1][current_column] = flow[current_flow_index]
            current_flow_index = current_flow_index + 1


    return flow_matrix

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
            parsed_year = dt.year - 190
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
