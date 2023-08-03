from flask import (
    request
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
import json
import re
from app.models import DataPoint, Probe, ProbeData, Graph
from sqlalchemy.sql import or_
import logging
_logger = logging.getLogger('')

class Mapping_Stub():
  def __init__(self):
    self.used_keys = []
  def get(self, key):
      if key not in self.used_keys:
        self.used_keys.append(key)
      return({
          'name': key
        })

class DataSet():
  def __init__(self):
    self.data = {}

  def push_coords(self, key, x, y):
    coords = {'x': x, 'y': y}
    try:
        self.data[key].append(coords)
    except KeyError as e:
      self.data[key] = [coords]

  def get_data_points(self):
    return self.data


class DataPointRetrieval(Resource):
  def post(self):
    request_json = request.get_json(force=True)
    graph_id = request_json.get('graph_id')
    probe_ids = request_json.get('probe_ids', [])
    probedata_ids = request_json.get('probedata_ids', [])
    start_time = request_json.get('start_time')
    end_time = request_json.get('end_time')
    zone_id = request_json.get('zone_id')
    limit = request_json.get('limit', 5000)
    if zone_id:
      query_result = Probe.query.filter(Probe.zone_id == zone_id).all()
      probe_ids_from_zone = list(map(lambda x: x.id, query_result))
      probe_ids.extend(probe_ids_from_zone)
    if graph_id:
      query_result = Graph.query.filter(Graph.id == graph_id).first()
      for line in query_result.graph_lines:
        probedata_ids.append(line.probedata_id)
    filters = []
    if start_time:
      filters.append(DataPoint.observation_datetime >= start_time)
    if end_time:
      filters.append(DataPoint.observation_datetime <= end_time)
    data = DataSet()
    query_result = ProbeData.query.filter(or_(ProbeData.probe_id.in_(probe_ids), ProbeData.id.in_(probedata_ids) ) ).all()
    probedatas = []
    for entry in query_result:
      probedatas.append(entry.as_dict())
    for probedata in probedatas:
      query_result = DataPoint.query.filter(DataPoint.probedata_id == probedata.get('id'), *filters).order_by(DataPoint.observation_datetime.desc()).limit(limit).all()
      for entry in query_result:
        long_key = probedata.get('name')
        value = entry.data
        timestamp = entry.observation_datetime.timestamp()
        data.push_coords(key=long_key, x=timestamp * 1000, y=value)
    return(data.get_data_points(), 200)
