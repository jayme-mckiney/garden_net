from flask import (
    request,
    jsonify
  )
from flask_restful import (
    Resource,
    abort,
    marshal
  )
from app.models import ProbeData, Zone, Probe
from app.db import db_session
import logging
_logger = logging.getLogger('')

class ProbeDataList(Resource):
  def get(self):
    results = ProbeData.query.all()
    dictionary_list = list(map(lambda r: r.as_dict(), results))
    return {'probe_datas': dictionary_list}, 200


class ProbeDataHeirarchy(Resource):
  def get(self):
    results = Zone.query.all()
    dictionary = {}
    for zone in results:
      dictionary[zone.id] = zone.as_dict()
      dictionary.get(zone.id)['probes'] = {}
      probes = dictionary.get(zone.id).get('probes')
      for probe in zone.probes:
        probes[probe.id] = probe.as_dict()
        probes.get(probe.id)['probe_datas'] = {}
        probe_datas = probes.get(probe.id).get('probe_datas')
        for probe_data in probe.probe_datas:
          probe_datas[probe_data.id] = probe_data.as_dict()
    return dictionary