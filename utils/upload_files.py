import numpy as np
import pandas as pd
from utils.matrix_convert import MatrixConversion
from calculations.AllMetrics import Metrics
from utils.constants import TYPES


def upload_files(start_date, files):
    output_files = 'output_files'

    for file in files:
        file_name = output_files + '/' + file.split('/')[1].split('.csv')[0]
        dataset = read_csv_to_arrays(file)
        matrix = MatrixConversion(
            dataset['date'], dataset['flow'], start_date)

        result = {}
        result["year_ranges"] = matrix.year_array
        result["flow_matrix"] = np.where(
            pd.isnull(matrix.flow_matrix), None, matrix.flow_matrix).tolist()

        write_to_csv(file_name, result, 'annual_flow_matrix')

        result["start_date"] = matrix.start_date

        calculated_metrics = Metrics(
            matrix.flow_matrix, matrix.years_array, None, None)

        result["DRH"] = calculated_metrics.drh

        write_to_csv(file_name, result, 'drh')

        result["all_year"] = {}
        result["all_year"]["average_annual_flows"] = calculated_metrics.average_annual_flows
        result["all_year"]["standard_deviations"] = calculated_metrics.standard_deviations
        result["all_year"]["coefficient_variations"] = calculated_metrics.coefficient_variations

        result["winter"] = {}
        result["winter"]["timings"] = calculated_metrics.winter_timings
        result["winter"]["durations"] = calculated_metrics.winter_durations
        result["winter"]["magnitudes"] = calculated_metrics.winter_magnitudes
        result["winter"]["frequencys"] = calculated_metrics.winter_frequencys

        result["fall"] = {}
        result["fall"]["timings"] = calculated_metrics.fall_timings
        result["fall"]["magnitudes"] = calculated_metrics.fall_magnitudes
        result["fall"]["wet_timings"] = calculated_metrics.fall_wet_timings
        result["fall"]["durations"] = calculated_metrics.fall_durations

        result["summer"] = {}
        result["summer"]["timings"] = calculated_metrics.summer_timings
        result["summer"]["magnitudes_ten"] = calculated_metrics.summer_10_magnitudes
        result["summer"]["magnitudes_fifty"] = calculated_metrics.summer_50_magnitudes
        result["summer"]["durations_flush"] = calculated_metrics.summer_flush_durations
        result["summer"]["durations_wet"] = calculated_metrics.summer_wet_durations
        result["summer"]["no_flow_counts"] = calculated_metrics.summer_no_flow_counts

        result["spring"] = {}
        result["spring"]["timings"] = calculated_metrics.spring_timings
        result["spring"]["magnitudes"] = calculated_metrics.spring_magnitudes
        result["spring"]["durations"] = calculated_metrics.spring_durations
        result["spring"]["rocs"] = calculated_metrics.spring_rocs

        result["fall_winter"] = {}
        result["fall_winter"]["baseflows"] = calculated_metrics.wet_baseflows

        write_to_csv(file_name, result, 'annual_flow_result')

    return True


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
        dict_to_array(result['winter'], 'winter', dataset)
        dict_to_array(result['fall'], 'fall', dataset)
        dict_to_array(result['summer'], 'summer', dataset)
        dict_to_array(result['spring'], 'spring', dataset)
        dict_to_array(result['fall_winter'], 'fall_winter', dataset)

        a = np.array(dataset)
        np.savetxt(file_name + '_' + file_type +
                   '.csv', a, delimiter=',', fmt='%s', header='Year, ' + year_ranges, comments='')


def dict_to_array(data, field_type, dataset):
    for key, value in data.items():
        if key != 'coefficient_variations':
            if field_type == 'winter':
                for k, v in value.items():
                    data = v
                    data.insert(0, TYPES[field_type+'_'+key+'_'+str(k)])
                    dataset.append(data)
            else:
                data = value
                data.insert(0, TYPES[field_type+'_'+key])
                dataset.append(data)


def read_csv_to_arrays(file_path):
    fields = ['date', 'flow']

    df = pd.read_csv(file_path, skipinitialspace=True, usecols=fields)

    dates = df['date']
    flow = df['flow']

    return {'date': dates, 'flow': flow}

# if path.splitext(file_path)[1] == '.csv':
#     with open(file_path, 'r') as csv_file:
#         reader = csv.reader(csv_file, delimiter=',')
#         if header:
#             return [row for index, row in enumerate(reader) if index > 0]
#         else:
#             return [row for row in reader]
