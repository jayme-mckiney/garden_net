from datetime import datetime
import time
import requests
from .models import Probe, DataPoint
from .db import db_session

"""
Sentry is a service that polls sensors configured through the webapp for data
"""

while True:
  active_probes = Probe.query().filter(Probe.active == True)
  for probe in active_probes:
    r = requests.get(probe.url)
    if r.status_code == 200:
      datapoint = DataPoint(observation_datetime = datetime.now(), probe_id = probe.id, data = r.json())
      db_session.add(datapoint)
    else:
      # log something
      print(f"recieved a non 200 response for {probe.name} at url: {probe.url}")
  db_session.commit()
  time.sleep(10)