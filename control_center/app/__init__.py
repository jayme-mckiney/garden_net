from flask import Flask, make_response
from flask_restful import Api
from flask_cors import CORS
import json
from .probe_config import ProbeConfig, ProbeList
from .zone_config import ZoneList
from .data_points import DataPointRetrieval
from logging.config import dictConfig
import logging

def create_app(db_session=None, debug=False):
  """Initialize the core application."""
  if debug is True:
    logging.getLogger('werkzeug').handlers.clear()
    logging.getLogger().handlers.clear()

  dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
      'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
      },
      "file": {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": "DEBUG",
        "filename": "/usr/logs/app.log",
        "when": "D",
        "interval": 1,
        "formatter": "default"
      }
    },
    'loggers': {
      '': {
          'level': 'DEBUG',
          'handlers': ['wsgi', 'file'],
      },
      "flask": {"level": "WARNING"},
      "sqlalchemy": {"level": "WARNING"},
      "werkzeug": {"level": "WARNING"},
    }
  })

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
  api.add_resource(ZoneList, '/zones')
  api.add_resource(DataPointRetrieval, '/data')
  return app