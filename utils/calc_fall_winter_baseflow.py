import numpy as np

def calc_fall_winter_baseflow(flow_matrix, fall_timings, fall_wet_timings, spring_timings):
    wet_baseflows_10 = []
    for column_number, spring_date in spring_timings:
        if spring_date and fall_wet_timings[column_number]:
            if fall_timings[column_number] and spring_date > fall_timings[column_number]:
                flow_data = flow_matrix[fall_timings[column_number]:spring_date, column_number]
            elif fall_wet_timings[column_number] and spring_date > fall_wet_timings[column_number]:
                flow_data = flow_matrix[fall_wet_timings[column_number]:spring_date, column_number]
            else:
                flow_data =[]
        else:
            flow_data = []

    if flow_data:
        wet_baseflows_10.append(np.nanpercentile(wet_baseflows_10, 10))
    else:
        wet_baseflows_10.append(None)

    return wet_baseflows_10
