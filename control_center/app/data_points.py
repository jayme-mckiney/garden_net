from flask import (
    request
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
import json
from models import DataPoint, Probe

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
    probe_ids = request_json.get('probe_ids', [])
    start_time = request_json.get('start_time')
    end_time = request_json.get('end_time')
    zone_id = request_json.get('zone_id')
    probes = list(map(lambda x: x.as_dict(), Probe.query.filter(Probe.id.in_(probe_ids)).all()))
    if zone_id:
      query_result = Probe.query.filter(Probe.zone_id == zone_id).all()
      probes_from_zone = list(map(lambda x: x.as_dict(), query_result))
      probes.extend(probes_from_zone)
    filters = []
    if start_time:
      filter.append(DataPoint.observation_datetime <= start_time)
    if end_time:
      filter.append(DataPoint.observation_datetime >= end_time)
    data = DataSet()
    for probe in probes:
      if probe.get('mappings'):
        mappings = probe.get('mappings')
      else:
        mappings = Mapping_Stub()
      query_result = DataPoint.query.filter(DataPoint.probe_id == probe.get('id'), *filters).order_by(DataPoint.observation_datetime).all()
      for entry in query_result:
        print(entry.data)
        for data_key, value in entry.data.items():
          long_key = f'{probe.get("name")}_{mappings.get(data_key).get("name")}'
          data.push_coords(key=long_key, x=entry.observation_datetime, y=value)
    return(data.get_data_points(), 200)