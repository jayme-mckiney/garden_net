from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import SingleDataMonitor
from app.db import db_session
import sqlalchemy
import logging
_logger = logging.getLogger('')

class MonitorList(Resource):
  def get(self):
    results = SingleDataMonitor.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'monitors': dictionary_list}, 200

  def post(self):
    json = request.get_json(force=True)
    try:
      new_monitor = SingleDataMonitor(**json.get('monitor'))
      db_session.add(new_monitor)
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

class MonitorConfig(Resource):
  def get(self, id):
    monitor = SingleDataMonitor.query.filter(SingleDataMonitor.id == id).first()
    if monitor == None:
      message = {'message': 'Monitor not found'}
      abort(404, **message)
    monitor_dict = monitor.as_dict()
    return ({'monitor': monitor_dict}, 200)

  def put(self, id):
    monitor = SingleDataMonitor.query.filter(SingleDataMonitor.id == id).first()
    json = request.get_json(force=True)
    if monitor == None:
      message = {'message': 'Monitor not found'}
      abort(404, **message)
    monitor_dict = monitor.as_dict()
    try:
      for key in monitor_dict:
        setattr(monitor, key, json.get('monitor').get(key))
      db_session.add(monitor)
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
    monitor = SingleDataMonitor.query.filter(SingleDataMonitor.id == id).first()
    if monitor == None:
      message = {'message': 'Monitor not found'}
      abort(404, **message)
    try:
      db_session.delete(monitor)
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