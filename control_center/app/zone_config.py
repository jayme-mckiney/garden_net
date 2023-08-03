from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import Zone
from app.db import db_session
import logging
_logger = logging.getLogger('')

class ZoneList(Resource):
  def get(self):
    results = Zone.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'zones': dictionary_list}, 200

  def post(self):
    json = request.get_json(force=True)
    try:
      new_zone = Zone(name=json.get('name'), description=json.get('description'))
      db_session.add(new_zone)
      db_session.commit()
    except TypeError as e:
      _logger.error(e)
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
    return ({}, 200)

class ZoneConfig(Resource):
  def get(self, id):
    zone = Zone.query.filter(Zone.id == id).first()
    if zone == None:
      message = {'message': 'Zone not found'}
      abort(404, **message)
    zone_dict = zone.as_dict()
    return ({'zone': zone_dict}, 200)

  def put(self, id):
    zone = Zone.query.filter(Zone.id == id).first()
    json = request.get_json(force=True)
    if zone == None:
      message = {'message': 'Zone not found'}
      abort(404, **message)
    try:
      setattr(zone, 'name', json['name'])
      setattr(zone, 'description', json['description'])
      db_session.add(zone)
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
    zone = Zone.query.filter(Zone.id == id).first()
    if zone == None:
      message = {'message': 'Zone not found'}
      abort(404, **message)
    try:
      db_session.delete(zone)
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