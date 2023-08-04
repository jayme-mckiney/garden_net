from app.models import ProbeData, SingleDataMonitor

def test_monitor_list(client, test_monitor_1):
  response = client.get('/monitors')
  assert response.status_code == 200
  assert response.get_json() == {
    'monitors': [test_monitor_1.as_dict()]
  }

def test_monitor_create_valid(client):
  probedata = ProbeData.query.first()
  response = client.post('/monitors', json={
    'monitor': {
      'name': 'test monitor 2',
      'probedata_id': probedata.id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': 15,
      'refresh_interval': 180
    }
    })
  assert response.status_code == 200
  monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  assert monitor.as_dict() == {
      'id': monitor.id,
      'name': 'test monitor 2',
      'probedata_id': probedata.id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': 15,
      'refresh_interval': 180
  }

def test_monitor_create_invalid_dupe_name(client, test_monitor_1):
  probedata = ProbeData.query.first()
  response = client.post('/monitors', json={
    'monitor': {
      'name': test_monitor_1.name,
      'probedata_id': probedata.id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': 15,
      'refresh_interval': 180
    }
  })
  assert response.status_code == 400

def test_monitor_create_invalid_blank_field(client):
  probedata = ProbeData.query.first()
  response = client.post('/monitors', json={
    'monitor': {
      'name': 'blah blah blah',
      'probedata_id': probedata.id,
      'tolerable_lower_bound': None,
      'tolerable_upper_bound': 15,
      'refresh_interval': 180
    }
  })
  assert response.status_code == 400

def test_monitor_edit_valid(client):
  monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  response = client.put('/monitors/{id}'.format(id=monitor.id), json={
    'monitor': {
      'id': monitor.id,
      'name': 'test monitor 2',
      'probedata_id': monitor.probedata_id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': 10,
      'refresh_interval': 180
    }
    })
  assert response.status_code == 200
  updated_monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  assert updated_monitor.tolerable_upper_bound == 10

def test_monitor_edit_invalid_name_dupe(client, test_monitor_1):
  monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  response = client.put('/monitors/{id}'.format(id=monitor.id), json={
    'monitor': {
      'id': monitor.id,
      'name': test_monitor_1.name,
      'probedata_id': monitor.probedata_id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': 15,
      'refresh_interval': 180
    }
    })
  assert response.status_code == 400

def test_monitor_edit_invalid_blank_field(client, test_monitor_1):
  monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  response = client.put('/monitors/{id}'.format(id=monitor.id), json={
    'monitor': {
      'id': monitor.id,
      'name': 'test monitor 2',
      'probedata_id': monitor.probedata_id,
      'tolerable_lower_bound': 5,
      'tolerable_upper_bound': None,
      'refresh_interval': 180
    }
    })
  assert response.status_code == 400

def test_monitor_get_single(client, test_monitor_1):
  response = client.get('/monitors/{id}'.format(id=test_monitor_1.id))
  assert response.status_code == 200
  assert response.get_json().get('monitor') == test_monitor_1.as_dict()

def test_monitor_get_single_nonexist(client):
  response = client.get('/monitors/100')
  assert response.status_code == 404

def test_monitor_delete(client):
  monitor = SingleDataMonitor.query.filter(SingleDataMonitor.name == 'test monitor 2').first()
  count_before = len(SingleDataMonitor.query.all())
  response = client.delete('/monitors/{id}'.format(id=monitor.id))
  assert response.status_code == 200
  count_after = len(SingleDataMonitor.query.all())
  assert count_after == count_before -1

def test_monitor_delete_nonexist(client):
  response = client.delete('/monitors/100')
  assert response.status_code == 404