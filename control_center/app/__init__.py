from flask import Flask, make_response
from flask_restful import Api
from flask_cors import CORS
import json
from .probe_config import ProbeConfig, ProbeList
from .data_monitor_config import MonitorConfig, MonitorList
from .graph_config import GraphConfig, GraphList
from .dashboard_config import DashboardList, DashboardConfig
from .probe_data_config import ProbeDataList, ProbeDataHeirarchy
from .zone_config import ZoneList, ZoneConfig
from .data_points import DataPointRetrieval
from logging.config import dictConfig
import logging

def create_app(db_session=None, debug=False):
  """Initialize the core application."""
  logging_level = 'INFO'
  if debug is True:
    logging.getLogger('werkzeug').handlers.clear()
    logging.getLogger().handlers.clear()
    logging_level = 'DEBUG'

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
          'level': logging_level,
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

  api.add_resource(ProbeDataList, '/probe_datas')
  api.add_resource(ProbeDataHeirarchy, '/probe_datas_structured')
  api.add_resource(ProbeList, '/probes')
  api.add_resource(ProbeConfig, '/probes/<id>')
  api.add_resource(ZoneList, '/zones')
  api.add_resource(ZoneConfig, '/zones/<id>')
  api.add_resource(DataPointRetrieval, '/data')
  api.add_resource(GraphList, '/graphs')
  api.add_resource(GraphConfig, '/graphs/<id>')
  api.add_resource(MonitorList, '/monitors')
  api.add_resource(MonitorConfig, '/monitors/<id>')
  api.add_resource(DashboardList, '/dashboards')
  api.add_resource(DashboardConfig, '/dashboards/<id>')
  return app