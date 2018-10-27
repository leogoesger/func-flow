from datetime import date, datetime
import csv
import numpy as np
import pandas as pd

from utils.helpers import is_two_digit_year, is_multiple_date_data, add_years, year_in_front


class MatrixConversion2:
    """Convert time series data to its matrix equvilant.

    Arguments:
        date_array {array} -- An array with date with the following format "mm/dd/yyyy"
        data_array {array} -- An array with data
        offset_date {string} -- A string following "mm/dd"

    """

    def __init__(self, date_array, data_array, offset_date="01/01"):
        self.date_array = date_array[1:]
        self.data_array = data_array[1:]
        self.offset_date = offset_date if offset_date else "01/01"
        self.julian_date_array = []

        self.start_year = None
        self.end_year = None
        self.final_matrix = None

        self.get_empty_matrix()
        self.populate()

    def get_year_limits(self):
        """Assign year limits which accounts for leap year at either end
        """
        d1 = datetime.strptime(self.date_array[0], '%m/%d/%Y')
        d_end = datetime.strptime(self.date_array[-1], '%m/%d/%Y')
        d_off_1 = datetime.strptime(
            "{}/{}".format(self.offset_date, d1.year), '%m/%d/%Y')
        d_off_end = datetime.strptime(
            "{}/{}".format(self.offset_date, d_end.year), '%m/%d/%Y')

        self.start_year = d1.year if d1 >= d_off_1 else d1.year - 1
        self.end_year = d_end.year if d_end >= d_off_end else d_end.year - 1

    def get_empty_matrix(self):
        """Create an empty matrix with fixed size using start year/end year
        """
        if not self.start_year:
            self.get_year_limits()
        self.final_matrix = [[None for y in range(
            self.end_year - self.start_year + 1)] for x in range(366)]

    def get_position_index(self, date):
        """[summary]

        Arguments:
            date {[string]} -- string of a date with format mm/dd/yyyy

        Returns:
            [number, number] -- index of row, column
        """

        if not self.start_year:
            self.get_year_limits()

        d_f = datetime.strptime(date, '%m/%d/%Y')
        offset_f = datetime.strptime(
            "{}/{}".format(self.offset_date, d_f.year), '%m/%d/%Y')

        column_index = d_f.year - \
            self.start_year if d_f >= offset_f else d_f.year - self.start_year - 1
        # 01/01 is day 1, so '-1' will give the index of array
        row_index = date_to_offset_julian(date, self.offset_date) - 1

        return row_index, column_index

    def populate(self):
        """Populate matrix with data
        """
        for index, d in enumerate(self.date_array):
            r_i, c_i = self.get_position_index(d)

            self.final_matrix[r_i][c_i] = self.data_array[index]


def date_to_julian(date):
    return datetime.strptime(date, '%m/%d/%Y').timetuple().tm_yday


def date_to_offset_julian(date, offset_date):
    """Convert date to offset julian date

    Arguments:
        date {string} -- A string following "mm/dd/YYYY"
        offset_date {string} -- A string following "mm/dd"

    Returns:
        {number} -- Offset julian date
    """

    date_formatted = datetime.strptime(date, '%m/%d/%Y')
    offset_formatted = datetime.strptime(
        "{}/{}".format(offset_date, date_formatted.year), '%m/%d/%Y')

    days_in_year = 366 if offset_formatted.year % 4 == 0 else 365

    date_julian = date_formatted.timetuple().tm_yday
    offset_julian = offset_formatted.timetuple().tm_yday

    if date_julian >= offset_julian:
        return date_julian - offset_julian + 1
    else:
        return date_julian + days_in_year - offset_julian + 1


class MatrixConversion:

    def __init__(self, date_array, flow_array,  start_date):
        self.flow_array = flow_array
        self.date_array = date_array
        self.start_date = start_date

        self.julian_array = []
        self.year_array = []  # Without duplicate, 1901, 1902, 1903
        self.years_array = []  # With duplicate, 1901, 1901, 1902, 1903
        self.flow_matrix = None
        self.get_date_arrays()
        self.get_flow_matrix()

    def get_date_arrays(self):

        for index, date in enumerate(self.date_array):

            current_date = datetime.strptime(date, "%m/%d/%Y")
            self.julian_array.append(current_date.timetuple().tm_yday)
            self.years_array.append(current_date.year)

            if index == 0:
                julian_start_date_first_year = datetime.strptime(
                    "{}/{}".format(self.start_date, current_date.year), "%m/%d/%Y").timetuple().tm_yday
                if(current_date.timetuple().tm_yday < julian_start_date_first_year):
                    first_year = current_date.year - 1
                else:
                    first_year = current_date.year

            if index == len(self.date_array) - 1:
                julian_start_date_last_year = datetime.strptime(
                    "{}/{}".format(self.start_date, current_date.year), "%m/%d/%Y").timetuple().tm_yday
                if(current_date.timetuple().tm_yday >= julian_start_date_last_year):
                    last_year = current_date.year + 1
                else:
                    last_year = current_date.year

        self.year_array = list(range(first_year, last_year))

    def get_position(self, year, julian_date, year_ranges, julian_start_date, days_in_year):
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

    def get_flow_matrix(self):

        number_of_columns = len(self.year_array)

        flow_matrix = np.zeros((366, number_of_columns))
        flow_matrix.fill(None)

        for index, julian_date in enumerate(self.julian_array):
            if(self.years_array[index] % 4 == 0):
                days_in_year = 366
            else:
                days_in_year = 365

            julian_start_date = datetime.strptime(
                "{}/{}".format(self.start_date, self.years_array[index]), "%m/%d/%Y").timetuple().tm_yday
            row, column = self.get_position(
                self.years_array[index], julian_date, self.year_array, julian_start_date, days_in_year)

            flow_matrix[row][column] = self.flow_array[index]

        self.flow_matrix = flow_matrix


def convert_raw_data_to_matrix(fixed_df, current_gauge_column_index, start_date):
    """Summary Function
    """

    current_gauge_class, current_gauge_number, raw_date_column, raw_flow_column = extract_current_data_at_index(
        fixed_df, current_gauge_column_index)

    date_column, flow_column = remove_nan_from_date_and_flow_columns(
        raw_date_column, raw_flow_column)

    years, julian_dates, number_of_years = extract_info_from_date(date_column)
    year_ranges = get_year_ranges_from_julian_dates(
        julian_dates, years, start_date)

    flow_matrix = get_flow_matrix(
        years, julian_dates, flow_column, year_ranges, start_date)
    return current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates


def extract_current_data_at_index(fixed_df, current_gauge_column_index):
    current_gauge_number = fixed_df.iloc[1, current_gauge_column_index]
    current_gauge_class = fixed_df.iloc[0, current_gauge_column_index]

    print(current_gauge_number, current_gauge_class)
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
    years = []
    julian_dates = []
    number_of_years = 0

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
            current_year = parsed_year
            number_of_years = number_of_years + 1

    return years, julian_dates, number_of_years


def get_year_ranges_from_julian_dates(julian_dates, years, start_date):
    julian_start_date_first_year = datetime.strptime(
        "{}/{}".format(start_date, years[0]), "%m/%d/%Y").timetuple().tm_yday
    julian_start_date_last_year = datetime.strptime(
        "{}/{}".format(start_date, years[-1]), "%m/%d/%Y").timetuple().tm_yday

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

        julian_start_date = datetime.strptime(
            "{}/{}".format(start_date, years[index]), "%m/%d/%Y").timetuple().tm_yday
        row, column = get_position(
            years[index], julian_date, year_ranges, julian_start_date, days_in_year)

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
        for rowIndex, value in enumerate(sorted_matrix[:, counter]):
            sorted_matrix[rowIndex, counter] = matrix[rowIndex][index]
        counter = counter + 1

    return sorted_matrix.tolist()


def insert_column_header(matrix, column_header):
    for index, name in enumerate(column_header):
        matrix[index].insert(0, name)
    return matrix
