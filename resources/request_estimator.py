# needs: pip install python-simplexml
from simplexml import dumps
from flask import make_response, request
from flask_restful import Resource
from resources.estimator import estimator
import json



def read_requests_logs():
  """ Opens saved_logs json file and return existing requests logs as list or empty list"""
  with open("saved_logs.json", "r+") as logs:
        try:
            data = json.load(logs)
        except Exception as e:
            print('error while loading json data', e)
            data = []
        # convert data to list if not
        if type(data) is dict:
            data = [data]
        return data

def update_requests_logs(request_details):
  """ append new request to requests logs file"""
  existing_requests = read_requests_logs()
  with open("saved_logs.json", "r+") as logs:
    existing_requests.append(request_details)
    # to reset the file pointer to position 0 
    logs.seek(0)
    json.dump(existing_requests, logs)




def getRequestElastedTime(elapsedDelta):
  # we convert datetime.timedelta(days, seconds, microseconds=) to ms
  return (elapsedDelta.days * 24 * 60 * 60 + elapsedDelta.seconds) * 1000 + elapsedDelta.microseconds / 1000.0


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

def writeResponseLines():
  return '\n'.join(['{method}  {path}       {status}  {duration}ms'.format(method=elt['method'], path=elt['path'], status=elt['status'], duration=elt['duration']) for elt in read_requests_logs()])


class GetEstimatorLogs(Resource):
  def get(self):
    response = make_response(writeResponseLines(), 200)
    response.headers['content-type'] = 'text/plain'
    return response