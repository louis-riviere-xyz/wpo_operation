def test_get_operation(client):
    response = client.get('/operation')
    assert response.status_code == 200
    ops = response.json()
    assert isinstance(ops, list)
    assert 'ChangeGearbox' in ops


def test_get_ChangeGearBox(client):
    response = client.get('/operation/ChangeGearbox')
    assert response.status_code == 200
    op = response.json()
    assert isinstance(op, dict)
    assert op['name'] == 'ChangeGearbox'


def test_get_missing(client):
    response = client.get('/operation/missing')
    assert response.status_code == 404
    err = response.json()
    assert err['detail'] == 'Operation not found : "missing".'
