from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import ProbeData
from app.db import db_session
import logging
_logger = logging.getLogger('')

class ProbeDataList(Resource):
  def get(self):
    results = ProbeData.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'probe_datas': dictionary_list}, 200

