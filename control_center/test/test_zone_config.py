def test_zone_list_intitial(client):
  response = client.get('/zones')
  assert response.status_code == 200
  assert response.get_json() == {"zones": [{'id': 1, 'name': 'Main', 'description': 'Primary grow zone'}]}

def test_zone_create(client):
  response = client.post('/zones', json={
    'name': 'test zone',
    'description': 'some zone thing'
  })
  assert response.status_code == 200
  response = client.get('/zones')
  assert len(response.get_json().get('zones')) == 2

def test_get_single_zone(client):
  response = client.get('/zones/2')
  assert response.status_code == 200
  assert response.get_json() == {
    'zone': {
      'id': 2,
      'name': 'test zone',
      'description': 'some zone thing'
    }
  }

def test_zone_delete(client):
  response = client.delete('/zones/2')
  assert response.get_json() == {}
  assert response.status_code == 200
  response = client.get('/zones/2')
  assert response.status_code == 404