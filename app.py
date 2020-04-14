from flask import Flask
from flask_restful import Api

from resources.request_estimator import GetEstimator, DefaultGetEstimator

app = Flask(__name__)
api = Api(app)

api.add_resource(DefaultGetEstimator, "/api/v1/on-covid-19")
api.add_resource(GetEstimator, "/api/v1/on-covid-19/<string:response_format>")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()