
def calc_fall_flush_timing(flow_matrix, start_of_summer):
    sigma = 10
    start_dates = []

    for column_number, column_flow in enumerate(flow_matrix[0]):

        """Summer baseflow determined by the previous year if not the first year"""
        if column_number == 0:
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[start_of_summer[0]:361, 0])
        elif start_of_summer[column_number - 1] and 361 > start_of_summer[column_number - 1]:
            summer_baseflow = 1.5 * np.nanmedian(flow_matrix[start_of_summer[column_number]:361, column_number - 1])

        flow_data = flow_matrix[:, column_number]
        x_axis = list(range(len(flow_data)))

        """Filter noise data"""
        filter_data = gaussian_filter1d(flow_data, sigma)

        for index, data in enumerate(filter_data):
            start_dates.append(index)
