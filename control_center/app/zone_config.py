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

  def post():
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
