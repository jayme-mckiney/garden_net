from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import Dashboard
from app.db import db_session
import sqlalchemy
import logging
_logger = logging.getLogger('')

class DashboardList(Resource):
  def get(self):
    results = Dashboard.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'dashboards': dictionary_list}, 200

  def post(self):
    json = request.get_json(force=True)
    try:
      new_dashboard = Dashboard(**json.get('dashboard'))
      db_session.add(new_dashboard)
      db_session.commit()
    except TypeError as e:
      _logger.error(e)
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except sqlalchemy.exc.IntegrityError as e:
      error_data = {'message': e.orig.args[1]}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
    return ({}, 200)

class DashboardConfig(Resource):
  def get(self, id):
    dashboard = Dashboard.query.filter(Dashboard.id == id).first()
    if dashboard == None:
      message = {'message': 'Dashboard not found'}
      abort(404, **message)
    dashboard_dict = dashboard.as_dict()
    return ({'dashboard': dashboard_dict}, 200)

  def put(self, id):
    dashboard = Dashboard.query.filter(Dashboard.id == id).first()
    json = request.get_json(force=True)
    if dashboard == None:
      message = {'message': 'Dashboard not found'}
      abort(404, **message)
    dashboard_dict = dashboard.as_dict()
    try:
      for key in dashboard_dict:
        setattr(dashboard, key, json.get('dashboard').get(key))
      db_session.add(dashboard)
      db_session.commit()
    except TypeError as e:
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except sqlalchemy.exc.IntegrityError as e:
      error_data = {'message': e.orig.args[1]}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
      _logger.error(e)
    return ({}, 200)

  def delete(self, id):
    dashboard = Dashboard.query.filter(Dashboard.id == id).first()
    if dashboard == None:
      message = {'message': 'Dashboard not found'}
      abort(404, **message)
    try:
      db_session.delete(dashboard)
      db_session.commit()
    except TypeError as e:
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except sqlalchemy.exc.IntegrityError as e:
      error_data = {'message': e.orig.args[1]}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
      _logger.error(e)
    return ({}, 200)