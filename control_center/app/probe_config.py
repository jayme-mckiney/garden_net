from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from models import Probe

class ProbeConfig(Resource):
  def get(self):
    id = request.args.get('id')
    query_result = Probe.query.filter(Probe.id == id).first()
    return {query_result.as_dict}

  def put(self, id):
    json = request.get_json(force=True)
    probe = Probe.query.filter_by(id=id).update(json)
    return {}, 200

class ProbeList(Resource):
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


