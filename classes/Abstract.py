from abc import ABC, abstractmethod
import os
import pandas as pd
from utils.helpers import is_multiple_date_data, find_index
from utils.matrix_convert import convert_raw_data_to_matrix
from classes.Gauge import Gauge
from pre_processFiles.gauge_reference import gauge_reference

class Abstract(ABC):
    percentilles = [10, 50, 90]

    def __init__(self, start_date, directory_name, end_with, class_number, gauge_numbers):
        self.start_date = start_date
        self.directory_name = directory_name
        self.end_with = end_with
        self.class_number = class_number
        self.gauge_numbers = gauge_numbers

        super().__init__()


    def _get_result_arrays(self, fixed_df, current_gauge_column_index):
        current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(
            fixed_df, current_gauge_column_index, self.start_date)
        self.general_info(current_gauge_class, current_gauge_number)
        if current_gauge_number in gauge_reference:
            start_year_index = find_index(year_ranges, int(gauge_reference[int(current_gauge_number)]['start']))
            end_year_index = find_index(year_ranges, int(gauge_reference[int(current_gauge_number)]['end']) + 1)
        else:
            print('Gauge {} Not Found'.format(current_gauge_number))
        current_gauge = Gauge(
            current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates, self.start_date, start_year_index, end_year_index)
        self.get_result_arrays(current_gauge)

    def calculate(self):
        for root, dirs, files in os.walk(self.directory_name):
            for file in files:
                if file.endswith(self.end_with):

                    fixed_df = pd.read_csv('{}/{}'.format(self.directory_name, file), sep=',',
                                           encoding='latin1', dayfirst=False, header=None, low_memory=False).dropna(axis=1, how='all')
                    step = is_multiple_date_data(fixed_df)

                    current_gauge_column_index = 1
                    if not self.class_number and not self.gauge_numbers:
                        while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                            self._get_result_arrays(fixed_df, current_gauge_column_index)
                            current_gauge_column_index = current_gauge_column_index + step

                    elif self.gauge_numbers:
                        while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                            if int(fixed_df.iloc[1, current_gauge_column_index]) in self.gauge_numbers:
                                self._get_result_arrays(fixed_df, current_gauge_column_index)
                            current_gauge_column_index = current_gauge_column_index + step

                    elif self.class_number:
                        while current_gauge_column_index <= (len(fixed_df.iloc[1, :]) - 1):
                            if int(fixed_df.iloc[0, current_gauge_column_index]) == int(self.class_number):
                                self._get_result_arrays(fixed_df, current_gauge_column_index)
                            current_gauge_column_index = current_gauge_column_index + step
                    else:
                        print('Something went wrong!')

        self.result_to_csv()

    @abstractmethod
    def get_result_arrays(self, current_gauge):
        raise NotImplementedError("Must override get_result_arrays")
    def general_info(self, current_gauge_class, current_gauge_number):
        raise NotImplementedError("Must override general_info")
    def result_to_csv(self):
        raise NotImplementedError("Must override result_to_csv")
