from flask import Blueprint, request, jsonify
from .ext import backend


api = Blueprint(
    'flask-profiling', __name__,
    url_prefix="/flask-profiling",
    static_folder="static/dist/", static_url_path='/static/dist')


@api.route("/")
def index():
    return api.send_static_file("index.html")


@api.route("/api/measurements/")
def filter_measurements():
    args = dict(request.args.items())
    measurements = backend.filter(args)
    return jsonify({"measurements": list(measurements)})


@api.route("/api/measurements/grouped")
def get_measurements_summary():
    args = dict(request.args.items())
    measurements = backend.get_summary(args)
    return jsonify({"measurements": list(measurements)})


@api.route("/api/measurements/<measurement_id>")
def getContext(measurement_id):
    return jsonify(backend.get(measurement_id))


@api.route("/api/measurements/timeseries/")
def get_requests_timeseries():
    args = dict(request.args.items())
    return jsonify({"series": backend.get_timeseries(args)})


@api.route("/api/measurements/method_distribution/")
def get_method_distribution():
    args = dict(request.args.items())
    return jsonify({"distribution": backend.get_method_distribution(args)})


@api.route("/db/dump")
def dumpDatabase():
    response = jsonify({
        "summary": backend.get_summary()})
    response.headers["Content-Disposition"] = "attachment; filename=dump.json"
    return response


@api.route("/db/delete")
def deleteDatabase():
    return jsonify({"status": backend.truncate()})


@api.after_request
def x_robots_tag_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    return response
