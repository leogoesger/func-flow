from datetime import datetime
from flask import request, jsonify
import simplejson
from app import app
from utils.matrix_convert import MatrixConversion
from utils.upload_files import get_result
from ml.RandomForest import RandomForest

rf = RandomForest()
rf.scale()
rf.impute()
rf.load()


@app.route('/api', methods=['GET', 'POST'])
def index():
    req_body = request.get_json()
    matrix = MatrixConversion(req_body["dates"],
                              req_body["flows"],  req_body["start_date"])

    julian_start_date = datetime.strptime(
        "{}/2001".format(req_body["start_date"]), "%m/%d/%Y").timetuple().tm_yday

    result = get_result(matrix, julian_start_date, req_body["params"])

    return jsonify(simplejson.dumps(result, ignore_nan=True)), 200


@app.route("/api/class-predict", methods=["POST"])
def predict():
    req_body = request.get_json()
    metric = req_body["metric"]
    predictions = rf.predict_s(metric)

    return jsonify(simplejson.dumps(predictions, ignore_nan=True)), 200
