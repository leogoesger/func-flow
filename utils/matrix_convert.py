from datetime import date, datetime
import csv
import numpy as np
import pandas as pd

from utils.helpers import is_two_digit_year, is_multiple_date_data, add_years, year_in_front

def convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date):
    """Summary Function
    """

    current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column = extract_current_data_at_index(fixed_df, current_gauge_column_index)

    date_column, flow_column = remove_nan_from_date_and_flow_columns(raw_date_column, raw_flow_column)

    years, julian_dates, number_of_years = extract_info_from_date(date_column)
    year_ranges = get_year_ranges_from_julian_dates(julian_dates, years, start_date)

    flow_matrix = get_flow_matrix(years, julian_dates, flow_column, year_ranges, start_date)
    return current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates

def extract_current_data_at_index(fixed_df, current_gauge_column_index):
    current_gauge_number = fixed_df.iloc[1, current_gauge_column_index]
    current_gauge_class = fixed_df.iloc[0, current_gauge_column_index]

    print('Gaguge Class: {}'.format(int(current_gauge_class)))
    print('Gauge Number: {}'.format(int(current_gauge_number)))

    if is_multiple_date_data(fixed_df):
        raw_date_column = fixed_df.iloc[:, current_gauge_column_index - 1]
    else:
        raw_date_column = fixed_df.iloc[:, 0]
    raw_flow_column = fixed_df.iloc[:, current_gauge_column_index]

    return current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column


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
    julian_dates=[]
    number_of_years=0

    current_year = 0
    for single_date in date:
        if is_two_digit_year(single_date):
            dt = datetime.strptime(single_date, "%m/%d/%y")
        elif year_in_front(single_date):
            dt = datetime.strptime(single_date, "%Y-%m-%d")
        else:
            dt = datetime.strptime(single_date, "%m/%d/%Y")

        if dt.year > 2019:
            parsed_year = dt.year - 100
        else:
            parsed_year = dt.year
        years.append(parsed_year)
        julian_dates.append(dt.timetuple().tm_yday)

        if parsed_year != current_year:
            current_year = parsed_year;
            number_of_years = number_of_years + 1

    return years, julian_dates, number_of_years

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
            """reduce by 100 when '88' is interpreted as 2088"""
            if current_date.year > 2015:
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

def sort_matrix(matrix, index):
    row = len(matrix)
    column = len(matrix[0])
    index_array = np.argsort(matrix[index])
    sorted_matrix = np.zeros((row, column))

    counter = 0
    for index in index_array:
        for rowIndex, value in enumerate(sorted_matrix[:,counter]):
            sorted_matrix[rowIndex,counter] = matrix[rowIndex][index]
        counter = counter + 1


    return sorted_matrix.tolist()

def insert_column_header(matrix, column_header):
    for index, name in enumerate(column_header):
        matrix[index].insert(0, name)
    return matrix
