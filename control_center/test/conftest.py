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
  GraphLine
)
    

@pytest.fixture(scope='module')
def client():
  db_session.bind = engine
  Base.metadata.bind = engine 
  drop_db()
  init_db()
  app = create_app(db_session)
  with app.test_client() as client:
    yield client
  drop_db()

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
  return probe

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

