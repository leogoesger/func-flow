import numpy as np

def calc_fall_winter_baseflow(flow_matrix, fall_flush_dates, fall_flush_wet_dates, spring_dates):
    wet_baseflows_10 = []
    for column_number, spring_date in spring_dates:
        if spring_date and fall_flush_wet_dates[column_number]:
            if fall_flush_dates[column_number] and spring_date > fall_flush_dates[column_number]:
                flow_data = flow_matrix[fall_flush_dates[column_number]:spring_date, column_number]
            elif fall_flush_wet_dates[column_number] and spring_date > fall_flush_wet_dates[column_number]:
                flow_data = flow_matrix[fall_flush_wet_dates[column_number]:spring_date, column_number]
            else:
                flow_data =[]
        else:
            flow_data = []

    if flow_data:
        wet_baseflows_10.append(np.nanpercentile(wet_baseflows_10, 10))
    else:
        wet_baseflows_10.append(None)

    return wet_baseflows_10
