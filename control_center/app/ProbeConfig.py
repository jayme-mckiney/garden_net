from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from ../models import Probe, ProbeDataMapping

class ProbeConfig(Resource):
  def post(self):
    json = request.get_json(force=True)
    try:
      new_probe = Probe( json )
      db_session.add(new_probe)
      db_session.commit()
    except TypeError as e:
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)

  def get(self):
    request.args