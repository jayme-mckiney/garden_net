from flask import (
    request,
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
import json
from models import DataPoint, Probe

class DataPointRetrieval(Resource):
  def post(self):
    request_json = request.get_json(force=True)
    probe_ids = request_json.get('probe_ids', [])
    start_time = request_json.get('start_time')
    end_time = request_json.get('end_time')
    zone_id = request_json.get('zone_id')
    if zone_id:
      query_result = Probe.query.filter(Probe.zone_id == zone_id).all()
      probe_ids.extend(list(map(lambda x: x.as_dict(), query_result)))
    filters = []
    if start_time:
      filter.append(DataPoint.observation_datetime <= start_time)
    if end_time:
      filter.append(DataPoint.observation_datetime >= end_time)
    results = {}
    for probe_id in probe_ids:
      query_result = DataPoint.query.filter(*filters).order_by(DataPoint.observation_datetime).all()
      results[probe_id] = list(map(lambda x: x.as_dict(), query_result))
    return(results, 200)