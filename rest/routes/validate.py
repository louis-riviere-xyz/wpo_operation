from json import load
from logging import error

from fastapi import APIRouter, HTTPException, Request

from backend.operation import Operation


validate = APIRouter(
    prefix = '/validate',
    tags   = ['validate'],
)


def bad_request(code, x):
    msg = f'REQ ERR {code} ! {x}'
    error(msg)
    raise HTTPException(
        status_code = 401,
        detail = msg,
    ) from x


@validate.post('',
    status_code = 200,
    description = 'Validate a request',
)
async def request(request: Request):
    req = await request.json()
    try:
        full = f'data/{req["operation_name"]}.json'
    except Exception as x:
        bad_request(111, x)

    try:
        data = load(open(full))
    except Exception as x:
        bad_request(222, x)

    try:
        operation = Operation()
        operation.load(data)
    except Exception as x:
        bad_request(333, x)

    try:
        response = operation.validate(req)
        return response
    except Exception as x:
        bad_request(444, x)
