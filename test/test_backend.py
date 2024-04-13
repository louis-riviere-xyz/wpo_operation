def test_level_10(operation, req_level_10):
    response = operation.validate(req_level_10)
    assert response['status'] == 'denied'
    assert 'Invalid level' in response['reasons']


def test_level_25(operation, req_level_25):
    response = operation.validate(req_level_25)
    assert response['status'] == 'accepted'


def test_level_40(operation, req_level_40):
    response = operation.validate(req_level_40)
    assert response['status'] == 'accepted'


def test_level_50(operation, req_level_50):
    response = operation.validate(req_level_50)
    assert response['status'] == 'denied'
    assert 'Invalid level' in response['reasons']

