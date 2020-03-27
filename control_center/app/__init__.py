from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import json
from .probe_config import ProbeConfig, ProbeList
from .data_points import DataPointRetrieval


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            #return int(obj.strftime('%s'))
            return str(obj)
        elif isinstance(obj, datetime.date):
            #return int(obj.strftime('%s'))
            return str(obj)
        return json.JSONEncoder.default(self, obj)




def create_app(db_session=None, debug=False):
  """Initialize the core application."""
  app = Flask(__name__)
  if debug:
    CORS(app)
  api = Api(app, catch_all_404s=True)
  app.json_encoder = CustomEncoder

  @app.teardown_appcontext
  def shutdown_session(exception=None):
    db_session.remove()

  api.add_resource(ProbeList, '/probes')
  api.add_resource(ProbeConfig, '/probes/<id>')
  api.add_resource(DataPointRetrieval, '/data')
  return app