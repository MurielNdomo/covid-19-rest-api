# needs: pip install python-simplexml
from simplexml import dumps
from flask import make_response, request
from flask_restful import Resource
from resources.estimator import estimator
import json


# outputs data according to the correct format
def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response' :data}), code)
    resp.headers.extend(headers or {})
    return resp

class GetEstimator(Resource):
  def post(self, response_format):
    data = estimator(request.get_json(force=True))
    if response_format == 'xml':
      response = make_response(dumps({'response' :data}), 200)
      response.headers['content-type'] = 'application/xml'
      return response
    return data 


class DefaultGetEstimator(Resource):
  def post(self):
    return estimator(request.get_json(force=True)), 200
    