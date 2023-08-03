def test_probe_list_single(client, test_probe_1, test_probe_2):
  response = client.get('/probes')
  assert response.status_code == 200
  assert response.get_json() == {"probes": [
    test_probe_1.as_dict(), 
    test_probe_2.as_dict()
    ]}

def test_probe_create_valid(client):
  response = client.post("/probes", json= {
    "probe": {
      "name": "test1",
      "description": "test",
      "url": "",
      "active": True,
      "zone_id": 1
    },
    "probe_data": [{
      "name": "test1",
      "name_in_probe": "testblah",
      "description": "blah blah"
    }]
  })
  assert response.status_code == 200

def test_probe_create_invalid_dupe_name(client, test_probe_1):
  response = client.post("/probes", json= {
    "probe": {
      "name": test_probe_1.name,
      "description": "test",
      "url": "",
      "active": True,
      "zone_id": 1
    },
    "probe_data": [{
      "name": "test2-2",
      "name_in_probe": "testblah",
      "description": "blah blah"
    }]
  })
  assert response.status_code == 400
  assert response.get_json() == {"message": "Duplicate entry '{name}' for key 'name'".format(name=test_probe_1.name)}

def test_probe_create_invalid_no_zone(client):
  response = client.post("/probes", json= {
    "probe": {
      "name": "test3",
      "description": "test",
      "url": "",
      "active": True,
      "zone_id": None
    },
    "probe_data": [{
      "name": "test3",
      "name_in_probe": "testblah",
      "description": "blah blah"
    }]
  })
  assert response.status_code == 400
  assert response.get_json() == {"message": "Column 'zone_id' cannot be null"}

def test_probe_edit_valid(client):
  response = client.put("/probes/3", json= {
    "probe": {
      "id": 3,
      "name": 'test test test test',
      "description": "lorem ipsum",
      "url": "",
      "active": True,
      "zone_id": 1
    },
    "probe_data": [{
      "id": 5,
      "name": "temp",
      "name_in_probe": "testblah",
      "description": "blah blah"
    }]
  })
  assert response.get_json() == {}
  assert response.status_code == 200

def test_probe_get_valid(client):
  response = client.get("/probes/3")
  assert response.status_code == 200
  assert response.get_json() == {
      "probe": {
      "id": 3,
      "name": "test test test test",
      "description": "lorem ipsum",
      "url": "",
      "active": True,
      "zone_id": 1
    },
    "probe_data": [{
      "id": 5,
      "name": "temp",
      "name_in_probe": "testblah",
      "description": "blah blah",
      "probe_id": 3
    }]
  }

def test_probe_list_multiple(client, test_probe_1, test_probe_2):
  response = client.get('/probes')
  assert response.status_code == 200
  assert response.get_json() == {
    "probes": [
      test_probe_1.as_dict(),
      test_probe_2.as_dict(),
      {
        "active": True,
        "description": "lorem ipsum",
        "id": 3,
        "name": "test test test test",
        "url": "",
        "zone_id": 1
      }
    ]
  }

def test_probe_delete(client, test_probe_1, test_probe_2):
  response = client.delete('/probes/3')
  assert response.status_code == 200
  response = client.get('/probes')
  assert response.get_json() == {
    "probes": [test_probe_1.as_dict(), test_probe_2.as_dict()]
  }