import itertools
import numpy as np
import pandas as pd
from flask import request, jsonify
import simplejson
from app import app
from utils.matrix_convert import MatrixConversion
from calculations.AllMetrics import Metrics
from utils.helpers import remove_offset_from_julian_date
from datetime import datetime


@app.route('/api', methods=['GET', 'POST'])
def index():
    req_body = request.get_json()
    matrix = MatrixConversion(req_body["dates"],
                              req_body["flows"],  req_body["start_date"])

    julian_start_date = datetime.strptime(
        "{}/2001".format(req_body["start_date"]), "%m/%d/%Y").timetuple().tm_yday

    result = {}
    result["year_ranges"] = matrix.year_array
    result["flow_matrix"] = np.where(
        pd.isnull(matrix.flow_matrix), None, matrix.flow_matrix).tolist()
    result["start_date"] = matrix.start_date

    calculated_metrics = Metrics(
        matrix.flow_matrix, matrix.years_array, None, None, req_body['params'])

    print(calculated_metrics)

    result["DRH"] = calculated_metrics.drh

    result["all_year"] = {}
    result["all_year"]["average_annual_flows"] = calculated_metrics.average_annual_flows
    result["all_year"]["standard_deviations"] = calculated_metrics.standard_deviations
    result["all_year"]["coefficient_variations"] = calculated_metrics.coefficient_variations

    result["winter"] = {}
    # Convert key from number to names
    key_maps = {2: "two", 5: "five", 10: "ten", 20: "twenty", 50: "fifty"}
    winter_timings = {}
    winter_durations = {}
    winter_magnitudes = {}
    winter_frequencys = {}
    for key, value in key_maps.items():
        winter_timings[value] = list(map(
            remove_offset_from_julian_date, calculated_metrics.winter_timings[key], itertools.repeat(julian_start_date)))
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
    result["fall"]["magnitudes"] = calculated_metrics.fall_magnitudes
    result["fall"]["wet_timings"] = calculated_metrics.fall_wet_timings
    result["fall"]["durations"] = calculated_metrics.fall_durations

    result["summer"] = {}
    result["summer"]["timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.summer_timings, itertools.repeat(julian_start_date)))
    result["summer"]["magnitudes_ten"] = calculated_metrics.summer_10_magnitudes
    result["summer"]["magnitudes_fifty"] = calculated_metrics.summer_50_magnitudes
    result["summer"]["durations_flush"] = calculated_metrics.summer_flush_durations
    result["summer"]["durations_wet"] = calculated_metrics.summer_wet_durations
    result["summer"]["no_flow_counts"] = calculated_metrics.summer_no_flow_counts

    result["spring"] = {}
    result["spring"]["timings"] = list(map(
        remove_offset_from_julian_date, calculated_metrics.spring_timings, itertools.repeat(julian_start_date)))
    result["spring"]["magnitudes"] = calculated_metrics.spring_magnitudes
    result["spring"]["durations"] = calculated_metrics.spring_durations
    result["spring"]["rocs"] = calculated_metrics.spring_rocs

    result["fall_winter"] = {}
    result["fall_winter"]["baseflows"] = calculated_metrics.wet_baseflows

    # print(json.dumps(result))
    return jsonify(simplejson.dumps(result, ignore_nan=True)), 200
