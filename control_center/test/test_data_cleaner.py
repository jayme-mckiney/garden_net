from app.db import db_session
from app.models import Probe, ProbeData, DataPoint
from data_cleaner import clean
import sqlalchemy as sa
from datetime import datetime, timedelta



def test_avg_before_clean(client, datapoints_for_cleaner):
  query = sa.select(sa.func.avg(DataPoint.data))
  results = db_session.execute(query).first()
  # (1404 * 50    +   156 * 10) / 1560
  assert results[0] == 46.0

def test_after_clean(client, datapoints_for_cleaner):
  start = datapoints_for_cleaner['start_time'] + timedelta(hours=1)
  clean(start_time=start, days=1)
  query = sa.select(sa.func.avg(DataPoint.data))
  results = db_session.execute(query).first()
  # (50 value * (120 - 12) entries + 10 value * (144 entries + 12 entries)) / 264
  assert results[0] == 26.363636363636363
  client.get('/zones') # without invoking client in the module pytest doesn't know to tear down

