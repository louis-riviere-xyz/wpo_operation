from json import load

from fastapi.testclient import TestClient
from pytest import fixture

from backend.operation import Operation
from rest.api import api


class Client:
    cli = TestClient(api)
    def get(self, *a, **k):
        return self.cli.get(*a, **k)

    def post(self, *a, **k):
        return self.cli.post(*a, **k)


@fixture
def operation():
    data = load(open('test/operation.json'))
    op = Operation()
    op.load(data)
    return op


@fixture
def client():
    return Client()


@fixture
def req_level_10():
    return load(open('test/req_10.json'))


@fixture
def req_level_25():
    return load(open('test/req_25.json'))


@fixture
def req_level_40():
    return load(open('test/req_40.json'))


@fixture
def req_level_50():
    return load(open('test/req_50.json'))
