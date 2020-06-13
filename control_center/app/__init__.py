from flask import Flask, make_response
from flask_restful import Api
from flask_cors import CORS
import json
from .probe_config import ProbeConfig, ProbeList
from .data_points import DataPointRetrieval



def create_app(db_session=None, debug=False):
  """Initialize the core application."""
  app = Flask(__name__)
  if debug:
    CORS(app)
  api = Api(app, catch_all_404s=True)


  @api.representation('application/json')
  def output_json(data, code, headers=None):
      resp = make_response(json.dumps(data, default=str), code)
      resp.headers.extend(headers or {})
      return resp

  @app.teardown_appcontext
  def shutdown_session(exception=None):
    db_session.remove()

  api.add_resource(ProbeList, '/probes')
  api.add_resource(ProbeConfig, '/probes/<id>')
  api.add_resource(DataPointRetrieval, '/data')
  return app