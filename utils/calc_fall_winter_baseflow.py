import numpy as np

def calc_fall_winter_baseflow(flow_matrix, fall_wet_timings, spring_timings):
    wet_baseflows_10 = []
    wet_baseflows_50 = []
    wet_bfl_durs = []
    for column_number, spring_date in enumerate(spring_timings):
        if spring_date and fall_wet_timings[column_number] and not np.isnan(spring_date) and not np.isnan(fall_wet_timings[column_number]):
            if fall_wet_timings[column_number] and spring_date > fall_wet_timings[column_number]:
                flow_data = flow_matrix[int(fall_wet_timings[column_number]):int(spring_date), column_number]
            else:
                flow_data = []
        else:
            flow_data = []

        flow_data = list(flow_data)
        if flow_data:
            wet_baseflows_10.append(np.nanpercentile(flow_data, 10))
            wet_baseflows_50.append(np.nanpercentile(flow_data, 50))
            wet_bfl_durs.append(len(flow_data))
        else:
            wet_baseflows_10.append(None)
            wet_baseflows_50.append(None)
            wet_bfl_durs.append(None)
    return wet_baseflows_10, wet_baseflows_50, wet_bfl_durs
