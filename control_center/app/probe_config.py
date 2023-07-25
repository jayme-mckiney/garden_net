from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import Probe, ProbeData
from app.db import db_session
import logging
_logger = logging.getLogger('')

class ProbeConfig(Resource):
  def get(self, id):
    query_result = Probe.query.filter(Probe.id == id).first()
    query_data_parts = ProbeData.query.filter(ProbeData.probe_id == id).all()
    data_parts = []
    for data_part in query_data_parts:
      data_parts.append(data_part.as_dict())
    probe_dict = query_result.as_dict()
    return {'probe': probe_dict, 'probe_data': data_parts}

  def put(self, id):
    json = request.get_json(force=True)
    probe = Probe.query.filter_by(id=id).first()
    data_parts = []
    if len(json.get('probe_data')) > 0:
      data_parts = ProbeData.query.filter(ProbeData.probe_id == id).all()
    probe_dict = probe.as_dict()
    try:
      for key in probe_dict:
        setattr(probe, key, json.get('probe').get(key))
      for new_data_part in json.get('probe_data'):
        _logger.info(new_data_part)
        if new_data_part.get('id') != None:
          for data_part in data_parts:
            if new_data_part.get('id') == data_part.id:
              setattr(data_part, 'name', new_data_part['name'])
              setattr(data_part, 'name_in_probe', new_data_part['name_in_probe'])
              setattr(data_part, 'description', new_data_part['description'])
              break
        else:
          _logger.info("making new entry")
          pd = ProbeData(
            probe_id=id,
            name=new_data_part.get('name'),
            name_in_probe=new_data_part.get('name_in_probe'),
            description=new_data_part.get('description')
          )
          db_session.add(pd)
      db_session.commit()
    except TypeError as e:
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
      _logger.error(error_data)
    return ({}, 200)

class ProbeList(Resource):
  def post(self):
    json = request.get_json(force=True)
    _logger.info(json)
    try:
      new_probe = Probe( **json.get('probe') )
      db_session.add(new_probe)
      db_session.commit()
      for data_part in json.get('probe_data'):
        new_data_part = ProbeData(**data_part)
        new_data_part.probe_id = new_probe.id
        db_session.add(new_data_part)
      db_session.commit()
    except TypeError as e:
      _logger.error(e)
      error_data = {'message': 'payload does no match db schema'}
      abort(400, **error_data)
    except Exception as e:
      error_data = {'message': 'Something went wrong'}
      abort(500, **error_data)
    return ({}, 200)

  def get(self):
    name = request.args.get('name')
    zone_id = request.args.get('zone_id')
    active = request.args.get('active')
    filters = []
    if zone_id:
      filters.append(Probe.zone_id == zone_id)
    if name:
      fuzzy_name = "%{}%".format(name)
      filters.append(Probe.name.like(fuzzy_name))
    if active is not None:
      filters.append(Probe.active == active)
    results = Probe.query.filter(*filters).all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'probes': dictionary_list}, 200


