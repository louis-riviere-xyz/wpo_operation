def test_req_level_10(client, req_level_10):
    r = client.post('/validate', json=req_level_10)
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'denied'
    assert 'Invalid level' in response['reasons']


def test_req_level_25(client, req_level_25):
    r = client.post('/validate', json=req_level_25)
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'accepted'


def test_req_level_40(client, req_level_40):
    r = client.post('/validate', json=req_level_40)
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'accepted'


def test_req_level_50(client, req_level_50):
    r = client.post('/validate', json=req_level_50)
    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'denied'
    assert 'Invalid level' in response['reasons']
