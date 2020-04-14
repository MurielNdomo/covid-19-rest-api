import datetime
import time
import json 

from flask import Flask, request, g
from flask_restful import Api

from resources.request_estimator import GetEstimator, DefaultGetEstimator, GetEstimatorLogs, update_requests_logs

app = Flask(__name__)
api = Api(app)

api.add_resource(DefaultGetEstimator, "/api/v1/on-covid-19")
api.add_resource(GetEstimator, "/api/v1/on-covid-19/<string:response_format>")
api.add_resource(GetEstimatorLogs, "/api/v1/on-covid-19/logs")


@app.before_request
def before_request():
   g.request_start_time = time.time()

@app.after_request
def after_request_func(response):

    """ 
    This function will run after a request, as long as no exceptions occur.
    It must take and return the same parameter - an instance of response_class.
    This is a good place to do some application cleanup.
    """
     # Get elapsed time in milliseconds
    elapsed = time.time() - g.request_start_time
    elapsed = int(round(1000 * elapsed))
    update_requests_logs(dict(method=request.method, path=request.path, status=response.status_code, duration=elapsed))
    return response

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()