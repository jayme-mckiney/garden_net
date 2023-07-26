from datetime import datetime
import time
import requests
from app.models import Probe, ProbeData, DataPoint
from app.db import db_session

"""
Sentry is a service that polls sensors configured through the webapp for data
"""

while True:
  active_probes = Probe.query.filter(Probe.active == True)
  for probe in active_probes:
    r = requests.get(f"http://{probe.url}/")
    if r.status_code == 200:
      probe_datas = ProbeData.query.filter(ProbeData.probe_id == probe.id).all()
      json = r.json()
      for probedata in probedatas:
        datapoint = DataPoint(observation_datetime = datetime.now(), probedata_id = probedata.id, data = json.get(probedata.name_in_probe))
        db_session.add(datapoint)
    else:
      # log something
      print(f"recieved a non 200 response for {probe.name} at url: {probe.url}")
  db_session.commit()
  time.sleep(60)