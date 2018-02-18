import os
import pandas as pd
from utils.helpers import is_multiple_date_data
from utils.calc_annual_flow_metrics import Gauge
from utils.matrix_convert import convert_raw_data_to_matrix


def annual_flow_matrix(start_date, directoryName, endWith, class_number, gauge_numbers):

    for root, dirs, files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):

                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',',
                                       encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')
                step = is_multiple_date_data(fixed_df);

                current_gaguge_column_index = 1

                if not class_number and not gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                            fixed_df, current_gaguge_column_index, start_date)

                        current_gauge = Gauge(
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                        # current_gauge.create_result_csv()
                        current_gauge.plot_dates()

                        current_gaguge_column_index = current_gaguge_column_index + step
                elif gauge_numbers:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[1, current_gaguge_column_index]) in gauge_numbers:
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                                fixed_df, current_gaguge_column_index, start_date)

                            current_gauge = Gauge(
                                current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            # current_gauge.create_result_csv()
                            current_gauge.plot_dates()

                        current_gaguge_column_index = current_gaguge_column_index + step

                elif class_number:
                    while current_gaguge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                        if int(fixed_df.iloc[0, current_gaguge_column_index]) == int(class_number):
                            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
                                fixed_df, current_gaguge_column_index, start_date)

                            current_gauge = Gauge(
                                current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, start_date)

                            # current_gauge.create_result_csv()
                            current_gauge.plot_dates()


                        current_gaguge_column_index = current_gaguge_column_index + step

                else:
                    print('Something went wrong!')
