import pytest

from app import create_app
from app.db import (
  engine,
  db_session,
  Base,
  init_db,
  drop_db
)
from app.models import (
  Probe,
  ProbeData,
  Graph,
  GraphLine,
  DataPoint,
  SingleDataMonitor,
  Dashboard
)
from datetime import datetime, timedelta
import json
    

@pytest.fixture(scope='module')
def client():
  db_session.bind = engine
  Base.metadata.bind = engine 
  drop_db()
  init_db()
  app = create_app(db_session)
  print('making client')
  with app.test_client() as client:
    yield client
  print('dropping db')
  drop_db()
  print('db dropped')
  db_session.close()
  print('context destroyed')

@pytest.fixture(scope='module')
def test_probe_1():
  probe1 = Probe(name='first test probe', description='blah blah', active=True, zone_id=1, url='')
  db_session.add(probe1)
  db_session.commit()
  pd1 = ProbeData(name='test data1', name_in_probe='thing1', description='', probe_id=probe1.id)
  pd2 = ProbeData(name='test data2', name_in_probe='thing2', description='', probe_id=probe1.id)
  db_session.add(pd1)
  db_session.add(pd2)
  db_session.commit()
  datapoint_list =[]
  start_time = datetime(year=2023, month=8, day=2)
  for i in range(20):
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd1.id, data=i))
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd2.id, data=i+20))
  db_session.add_all(datapoint_list)
  db_session.commit()
  return probe1

@pytest.fixture(scope='module')
def test_probe_2():
  probe = Probe(name='second test probe', description='blah blah', active=True, zone_id=1, url='')
  db_session.add(probe)
  db_session.commit()
  pd3 = ProbeData(name='test data3', name_in_probe='thing3', description='', probe_id=probe.id)
  pd4 = ProbeData(name='test data4', name_in_probe='thing4', description='', probe_id=probe.id)
  db_session.add(pd3)
  db_session.add(pd4)
  db_session.commit()
  datapoint_list =[]
  start_time = datetime(year=2023, month=8, day=2)
  for i in range(20):
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd3.id, data=i+40))
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd4.id, data=i+60))
  db_session.add_all(datapoint_list)
  db_session.commit()
  return probe

@pytest.fixture(scope='module')
def test_monitor_1(test_probe_1):
  monitor = SingleDataMonitor(
    name = 'test monitor',
    probedata_id = test_probe_1.probe_datas[0].id,
    tolerable_lower_bound = 6,
    tolerable_upper_bound = 12,
    refresh_interval = 120
    )
  db_session.add(monitor)
  db_session.commit()
  return monitor

@pytest.fixture(scope='module')
def test_graph_1(test_probe_1):
  graph = Graph(name='first test graph', description='blah blah')
  db_session.add(graph)
  db_session.commit()
  gl1 = GraphLine(graph_id= graph.id, probedata_id=test_probe_1.probe_datas[0].id)
  gl2 = GraphLine(graph_id= graph.id, probedata_id=test_probe_1.probe_datas[1].id)
  db_session.add(gl1)
  db_session.add(gl2)
  db_session.commit()
  return graph


@pytest.fixture(scope='module')
def start_time():
  return datetime(year=2023, month=8, day=2)

@pytest.fixture(scope='module')
def test_dashboard(test_graph_1, test_monitor_1):
  dash = Dashboard(name='test dashboard', description="does stuff", layout=json.dumps([
      {
        'component_id': test_graph_1.id,
        'component_type': 'Graph',
        'sizing': {'width': '75%'}
      },
      {
        'component_id': test_monitor_1.id,
        'component_type': 'Monitor',
        'sizing': {'width': '25%'}
      }
    ]))
  db_session.add(dash)
  db_session.commit()
  return dash

@pytest.fixture(scope='module')
def datapoints_for_cleaner():
  probe1 = Probe(name='cleaner test probe1', description='cleaner test', active=True, zone_id=1, url='')
  db_session.add(probe1)
  db_session.commit()
  pd1 = ProbeData(name='cleaner test data1', name_in_probe='thing1', description='', probe_id=probe1.id)
  pd2 = ProbeData(name='cleeaner test data2', name_in_probe='thing2', description='', probe_id=probe1.id)
  db_session.add(pd1)
  db_session.add(pd2)
  db_session.commit()
  datapoint_list =[]
  start_time = datetime(year=2023, month=8, day=2) - timedelta(hours=1)
  for i in range(60*26):
    data = 50
    if i % 10 == 0:
      data = 10
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd1.id, data=data))
    datapoint_list.append(DataPoint(observation_datetime=start_time + timedelta(minutes=i), probedata_id=pd2.id, data=data))
  db_session.add_all(datapoint_list)
  db_session.commit()
  return {'probe': probe1, 'start_time': start_time}
  