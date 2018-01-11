import numpy as np
import csv
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

            if row[flow_index] == "":
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

        if sheet.cell(row, flow_index).value == "":
            flow.append(None)
        else:
            flow.append(sheet.cell(row, flow_index).value)


        if parsed_year != current_year:
            current_year = parsed_year
            number_of_years = number_of_years + 1
    return year, julian_date, flow, number_of_years

def convert_raw_data_to_matrix(path):
    """Return one matrix containing flow data for raw dataset

    """
    years, julian_dates, flow, number_of_years = import_and_parse_csv(path)


    flow_matrix = np.zeros((366, number_of_years))
    flow_matrix.fill(None)
    current_column = 0
    current_flow_index = 0
    current_year = years[0]

    print(julian_dates)

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
