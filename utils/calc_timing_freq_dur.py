def calculate_timing_duration_frequency(matrix, year_ranges, threshold):

    for column_number, flow in enumerate(matrix[0]):
        date_array = []
        flow_array = []
        for row_number, flow in enumerate(matrix[:, column_number]):
            if matrix[row_number, column_number] >= threshold:
                date_array.append()
                flow_array.append(matrix[row_number, column_number])

    return std
