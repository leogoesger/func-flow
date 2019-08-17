from datetime import datetime
import itertools
import numpy as np
import pandas as pd
from utils.matrix_convert import MatrixConversion
from calculations.AllMetrics import Metrics
from utils.constants import TYPES
from utils.helpers import remove_offset_from_julian_date


def upload_files(start_date, files):
    output_files = 'user_output_files'

    for file in files:
        file_name = output_files + '/' + file.split('/')[1].split('.csv')[0]
        dataset = read_csv_to_arrays(file)
        matrix = MatrixConversion(
            dataset['date'], dataset['flow'], start_date)

        julian_start_date = datetime.strptime(
            "{}/2001".format(start_date), "%m/%d/%Y").timetuple().tm_yday

        result = get_result(matrix, julian_start_date, None)

        write_to_csv(file_name, result, 'annual_flow_matrix')
        write_to_csv(file_name, result, 'drh')
        write_to_csv(file_name, result, 'annual_flow_result')

    return True


def get_result(matrix, julian_start_date, params):

    result = {}
    result["year_ranges"] = [int(i) + 1 for i in matrix.year_array]
    result["flow_matrix"] = np.where(
        pd.isnull(matrix.flow_matrix), None, matrix.flow_matrix).tolist()
    result["start_date"] = matrix.start_date

    calculated_metrics = Metrics(
        matrix.flow_matrix, matrix.years_array, None, None, params)

    result["DRH"] = calculated_metrics.drh

    result["all_year"] = {}
    result["all_year"]["average_annual_flows"] = calculated_metrics.average_annual_flows
    result["all_year"]["standard_deviations"] = calculated_metrics.standard_deviations
    result["all_year"]["coefficient_variations"] = calculated_metrics.coefficient_variations

    result["winter"] = {}
    # Convert key from number to names

    key_maps = {2: "two", 5: "five", 10: "ten", 20: "twenty", 50: "fifty", }
    # key_maps = {2: "two", 5: "five", 10: "ten", 20: "twenty", 12: "_two", 15: "_five", 110: "_ten", 120: "_twenty"}

    winter_timings = {}
    winter_durations = {}
    winter_magnitudes = {}
    winter_frequencys = {}
    for key, value in key_maps.items():
        winter_timings[value] = list(map(
            remove_offset_from_julian_date, calculated_metrics.winter_timings[key], itertools.repeat(julian_start_date)))
        winter_timings[value +
                       '_water'] = calculated_metrics.winter_timings[key]
        winter_durations[value] = calculated_metrics.winter_durations[key]
        winter_magnitudes[value] = calculated_metrics.winter_magnitudes[key]
        winter_frequencys[value] = calculated_metrics.winter_frequencys[key]

    result["winter"]["timings"] = winter_timings
    result["winter"]["durations"] = winter_durations
    result["winter"]["magnitudes"] = winter_magnitudes
    result["winter"]["frequencys"] = winter_frequencys

    result["fall"] = {}
    result["fall"]["timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.fall_timings, itertools.repeat(julian_start_date)))
    result["fall"]["timings_water"] = calculated_metrics.fall_timings
    result["fall"]["magnitudes"] = calculated_metrics.fall_magnitudes
    result["fall"]["wet_timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.fall_wet_timings, itertools.repeat(julian_start_date)))
    result["fall"]["wet_timings_water"] = calculated_metrics.fall_wet_timings
    result["fall"]["durations"] = calculated_metrics.fall_durations

    result["summer"] = {}
    result["summer"]["timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.summer_timings, itertools.repeat(julian_start_date)))
    result["summer"]["timings_water"] = calculated_metrics.summer_timings
    result["summer"]["magnitudes_ninety"] = calculated_metrics.summer_90_magnitudes
    result["summer"]["magnitudes_fifty"] = calculated_metrics.summer_50_magnitudes
    result["summer"]["durations_flush"] = calculated_metrics.summer_flush_durations
    result["summer"]["durations_wet"] = calculated_metrics.summer_wet_durations
    result["summer"]["no_flow_counts"] = calculated_metrics.summer_no_flow_counts

    result["spring"] = {}
    result["spring"]["timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.spring_timings, itertools.repeat(julian_start_date)))
    result["spring"]["timings_water"] = calculated_metrics.spring_timings
    result["spring"]["magnitudes"] = calculated_metrics.spring_magnitudes
    result["spring"]["durations"] = calculated_metrics.spring_durations
    result["spring"]["rocs"] = calculated_metrics.spring_rocs

    result["wet"] = {}
    result["wet"]["baseflows_10"] = calculated_metrics.wet_baseflows_10
    result["wet"]["baseflows_50"] = calculated_metrics.wet_baseflows_50
    result["wet"]["bfl_durs"] = calculated_metrics.wet_bfl_durs

    return result


def write_to_csv(file_name, result, file_type):
    year_ranges = ",".join(str(year) for year in result['year_ranges'])

    if file_type == 'annual_flow_matrix':

        a = np.array(result['flow_matrix'])
        np.savetxt(file_name + '_' + file_type + '.csv', a, delimiter=',',
                   header=year_ranges, fmt='%s', comments='')

    if file_type == 'drh':
        dataset = []
        for key, value in result['DRH'].items():
            data = value
            data.insert(0, key)
            dataset.append(data)

        a = np.array(dataset)
        np.savetxt(file_name + '_' + file_type +
                   '.csv', a, delimiter=',', fmt='%s', comments='')

    if file_type == 'annual_flow_result':

        dataset = []
        dict_to_array(result['all_year'], 'all_year', dataset)
        dict_to_array(result['spring'], 'spring', dataset)
        dict_to_array(result['summer'], 'summer', dataset)
        dict_to_array(result['fall'], 'fall', dataset)
        dict_to_array(result['wet'], 'wet', dataset)
        dict_to_array(result['winter'], 'winter', dataset)
        a = np.array(dataset)
        np.savetxt(file_name + '_' + file_type + '.csv', a, delimiter=',',
                   fmt='%s', header='Year, ' + year_ranges, comments='')


def dict_to_array(data, field_type, dataset):
    for key, value in data.items():
        if field_type == 'winter':
            for k, v in value.items():
                if k.find('timings') > -1:
                    continue
                data = v
                if k.find('_water') > -1:
                    tmp = k.split('_water')[0]
                    data.insert(
                        0, TYPES[field_type+'_'+key+'_'+str(tmp)] + '_Water')
                else:
                    data.insert(0, TYPES[field_type+'_'+key+'_'+str(k)])
                dataset.append(data)
        elif field_type == "summer":
            data = value
            if 'water' in key:
                tmp = key.split('_water')[0]
                data.insert(0, TYPES[field_type+'_'+tmp] + '_Water')
            elif 'durations_flush' in key:
                continue
            else:
                data.insert(0, TYPES[field_type+'_'+key])
            dataset.append(data)
        else:
            data = value
            if 'water' in key:
                tmp = key.split('_water')[0]
                data.insert(0, TYPES[field_type+'_'+tmp] + '_Water')
            else:
                data.insert(0, TYPES[field_type+'_'+key])
            dataset.append(data)


def read_csv_to_arrays(file_path):
    fields = ['date', 'flow']

    df = pd.read_csv(file_path, skipinitialspace=True, usecols=fields)

    dates = df['date']
    flow = df['flow']

    return {'date': dates, 'flow': flow}
