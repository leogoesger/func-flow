import numpy as np
from helpers import get_date_from_offset_julian_date

def calculate_timing_duration_frequency(matrix, year_ranges, start_date):

    two_timing_median = []
    two_duration_median = []
    two_frequency = []

    five_timing_median = []
    five_duration_median = []
    five_frequency = []

    ten_timing_median = []
    ten_duration_median = []
    ten_frequency = []

    twenty_timing_median = []
    twenty_duration_median = []
    twenty_frequency = []

    fifty_timing_median = []
    fifty_duration_median = []
    fifty_frequency = []

    for column_number, flow in enumerate(matrix[0]):
        two_date_array = []
        two_flow_array = []

        five_date_array = []
        five_flow_array = []

        ten_date_array = []
        ten_flow_array = []

        twenty_date_array = []
        twenty_flow_array = []

        fifty_date_array = []
        fifty_flow_array = []

        for row_number, flow in enumerate(matrix[:, column_number]):
            if matrix[row_number, column_number] >= np.nanpercentile(matrix[:,column_number], 98):
                two_date_array.append(get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date))
                two_flow_array.append(matrix[row_number, column_number])
            elif matrix[row_number, column_number] >= np.nanpercentile(matrix[:,column_number], 95):
                five_date_array.append(get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date))
                five_flow_array.append(matrix[row_number, column_number])
            elif matrix[row_number, column_number] >= np.nanpercentile(matrix[:,column_number], 90):
                ten_date_array.append(get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date))
                ten_flow_array.append(matrix[row_number, column_number])
            elif matrix[row_number, column_number] >= np.nanpercentile(matrix[:,column_number], 80):
                twenty_date_array.append(get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date))
                twenty_flow_array.append(matrix[row_number, column_number])
            elif matrix[row_number, column_number] >= np.nanpercentile(matrix[:,column_number], 50):
                fifty_date_array.append(get_date_from_offset_julian_date(row_number, year_ranges[column_number], start_date))
                fifty_flow_array.append(matrix[row_number, column_number])

        two_start_date_array = []
        two_duration_array = []
        two_frequency_current = 0

        two_previous_date = 0
        two_duration = 1

        for index, date in enumerate(two_date_array):
            if date.timetuple().tm_yday - two_previous_date > 1:
                two_start_date_array.append(date.timetuple().tm_yday)
                two_previous_date = date.timetuple().tm_yday
                two_frequency_current = two_frequency_current + 1
                if index != 0:
                    two_duration_array.append(two_duration)
                    two_duration = 1
                if index == len(two_date_array) - 1:
                    two_duration_array.append(two_duration)

            elif date.timetuple().tm_yday - two_previous_date == 1:
                two_duration = two_duration + 1
                if index == len(two_date_array) - 1:
                    two_duration_array.append(two_duration)

        two_timing_median.append(np.nanmean(two_start_date_array))
        two_duration_median.append(np.nanmean(two_duration_array))
        two_frequency.append(two_frequency_current)


        five_start_date_array = []
        five_duration_array = []
        five_frequency_current = 0

        five_previous_date = 0
        five_duration = 1

        for index, date in enumerate(five_date_array):
            if date.timetuple().tm_yday - five_previous_date > 1:
                five_start_date_array.append(date.timetuple().tm_yday)
                five_previous_date = date.timetuple().tm_yday
                five_frequency_current = five_frequency_current + 1
                if index != 0:
                    five_duration_array.append(five_duration)
                    five_duration = 1
                if index == len(five_date_array) - 1:
                    five_duration_array.append(five_duration)

            elif date.timetuple().tm_yday - five_previous_date == 1:
                five_duration = five_duration + 1
                if index == len(five_date_array) - 1:
                    five_duration_array.append(five_duration)

        five_timing_median.append(np.nanmean(five_start_date_array))
        five_duration_median.append(np.nanmean(five_duration_array))
        five_frequency.append(five_frequency_current)

        ten_start_date_array = []
        ten_duration_array = []
        ten_frequency_current = 0

        ten_previous_date = 0
        ten_duration = 1

        for index, date in enumerate(ten_date_array):
            if date.timetuple().tm_yday - ten_previous_date > 1:
                ten_start_date_array.append(date.timetuple().tm_yday)
                ten_previous_date = date.timetuple().tm_yday
                ten_frequency_current = ten_frequency_current + 1
                if index != 0:
                    ten_duration_array.append(ten_duration)
                    ten_duration = 1
                if index == len(ten_date_array) - 1:
                    ten_duration_array.append(ten_duration)

            elif date.timetuple().tm_yday - ten_previous_date == 1:
                ten_duration = ten_duration + 1
                if index == len(ten_date_array) - 1:
                    ten_duration_array.append(ten_duration)

        ten_timing_median.append(np.nanmean(ten_start_date_array))
        ten_duration_median.append(np.nanmean(ten_duration_array))
        ten_frequency.append(ten_frequency_current)

        twenty_start_date_array = []
        twenty_duration_array = []
        twenty_frequency_current = 0

        twenty_previous_date = 0
        twenty_duration = 1

        for index, date in enumerate(twenty_date_array):
            if date.timetuple().tm_yday - twenty_previous_date > 1:
                twenty_start_date_array.append(date.timetuple().tm_yday)
                twenty_previous_date = date.timetuple().tm_yday
                twenty_frequency_current = twenty_frequency_current + 1
                if index != 0:
                    twenty_duration_array.append(twenty_duration)
                    twenty_duration = 1
                if index == len(twenty_date_array) - 1:
                    twenty_duration_array.append(twenty_duration)

            elif date.timetuple().tm_yday - twenty_previous_date == 1:
                twenty_duration = twenty_duration + 1
                if index == len(twenty_date_array) - 1:
                    twenty_duration_array.append(twenty_duration)

        twenty_timing_median.append(np.nanmean(twenty_start_date_array))
        twenty_duration_median.append(np.nanmean(twenty_duration_array))
        twenty_frequency.append(twenty_frequency_current)

        fifty_start_date_array = []
        fifty_duration_array = []
        fifty_frequency_current = 0

        fifty_previous_date = 0
        fifty_duration = 1

        for index, date in enumerate(fifty_date_array):
            if date.timetuple().tm_yday - fifty_previous_date > 1:
                fifty_start_date_array.append(date.timetuple().tm_yday)
                fifty_previous_date = date.timetuple().tm_yday
                fifty_frequency_current = fifty_frequency_current + 1
                if index != 0:
                    fifty_duration_array.append(fifty_duration)
                    fifty_duration = 1
                if index == len(fifty_date_array) - 1:
                    fifty_duration_array.append(fifty_duration)

            elif date.timetuple().tm_yday - fifty_previous_date == 1:
                fifty_duration = fifty_duration + 1
                if index == len(fifty_date_array) - 1:
                    fifty_duration_array.append(fifty_duration)

        fifty_timing_median.append(np.nanmean(fifty_start_date_array))
        fifty_duration_median.append(np.nanmean(fifty_duration_array))
        fifty_frequency.append(fifty_frequency_current)


    return two_timing_median, two_duration_median, two_frequency, five_timing_median, five_duration_median, five_frequency, ten_timing_median, ten_duration_median, ten_frequency, twenty_timing_median, twenty_duration_median, twenty_frequency, fifty_timing_median, fifty_duration_median, fifty_frequency,
