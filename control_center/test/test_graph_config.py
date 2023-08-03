from app.models import ProbeData, Graph

def test_graph_list(client, test_graph_1):
  response = client.get('/graphs')
  assert response.status_code == 200
  assert response.get_json() == {"graphs": [test_graph_1.as_dict()]}

def test_graph_create(client, test_probe_2):
  response = client.post('/graphs', json={
    'graph': {
      'name': 'test graph',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'probedata_id': test_probe_2.probe_datas[0].id},
      {'probedata_id': test_probe_2.probe_datas[1].id}
    ]
  })
  assert response.status_code == 200
  response = client.get('/graphs')
  assert len(response.get_json().get('graphs')) == 2

def test_get_single_graph(client, test_probe_2):
  response = client.get('/graphs/2')
  assert response.status_code == 200
  assert response.get_json() == {
    'graph': {
      'id': 2,
      'name': 'test graph',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[0].id},
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[1].id}
    ]
  }

def test_graph_edit(client, test_probe_2):
  response = client.put('graphs/2', json={
    'graph': {
      'id': 2,
      'name': 'test graph alteration',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[0].id}
    ]
  })
  assert response.status_code == 200
  response = client.get('/graphs/2')
  assert response.get_json() == {
    'graph': {
      'id': 2,
      'name': 'test graph alteration',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[0].id}
    ]
  }
  response = client.put('graphs/2', json={
    'graph': {
      'id': 2,
      'name': 'test graph alteration',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[0].id},
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[1].id}
    ]
  })
  assert response.status_code == 200
  response = client.get('/graphs/2')
  assert response.get_json() == {
    'graph': {
      'id': 2,
      'name': 'test graph alteration',
      'description': 'some graph thing'
    },
    'graph_lines': [
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[0].id},
      {'graph_id': 2, 'probedata_id': test_probe_2.probe_datas[1].id}
    ]
  }

def test_graph_delete(client):
  response = client.delete('/graphs/2')
  assert response.get_json() == {}
  assert response.status_code == 200
  response = client.get('/graphs/2')
  assert response.status_code == 404

