from app.models import Dashboard, SingleDataMonitor, Graph

def test_dashboard_list(client, test_dashboard):
  response = client.get('/dashboards')
  assert response.status_code == 200
  assert response.get_json() == {
    'dashboards': [test_dashboard.as_dict()]
  }

def test_dashboard_create_valid(client):
  payload = {
    'name': 'dashboard 2',
    'description': 'lorem ipsum',
    'layout': [
      {
        'component_id': 5,
        'component_type': 'graph',
        'sizing': {'width': '100%'}
      }
    ]
  }
  response = client.post('/dashboards', json={'dashboard': payload})
  assert response.status_code == 200
  dashboards = Dashboard.query.all()
  assert len(dashboards) == 2
  assert dashboards[1].name == payload['name']
  assert dashboards[1].description == payload['description']
  assert dashboards[1].layout == payload['layout']

def test_dashboard_create_invalid(client):
  payload = {
    'name': 'dashboard 2',
    'description': 'lorem ipsum',
    'layout': [
      {
        'component_id': 5,
        'component_type': 'graph',
        'sizing': {'width': '100%'}
      }
    ]
  }
  response = client.post('/dashboards', json={'dashboard': payload})
  assert response.status_code == 400

def test_dashboard_edit(client):
  payload = {
    'id': 2,
    'name': 'dashboard 2',
    'description': 'lorem ipsum',
    'layout': [
      {
        'component_id': 6,
        'component_type': 'graph',
        'sizing': {'width': '75%'}
      },
      {
        'component_id': 4,
        'component_type': 'monitor',
        'sizing': {'width': '25%'}
      }
    ]
  }
  response = client.put('/dashboards/2', json={'dashboard': payload})
  assert response.status_code == 200
  dashboard = Dashboard.query.filter(Dashboard.id == 2).first()
  assert dashboard.as_dict() == payload

def test_dashboard_delete(client):
  response = client.delete('/dashboards/2')
  assert response.status_code == 200
  dashboards = Dashboard.query.all()
  assert len(dashboards) == 1

def test_dashboard_delete_nonexistant(client):
  response = client.delete('/dashboards/3')
  assert response.status_code == 404
  dashboards = Dashboard.query.all()
  assert len(dashboards) == 1
