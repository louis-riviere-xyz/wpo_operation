from json import load, dump
from logging import error
from pathlib import Path
from os import listdir

from fastapi import APIRouter, HTTPException


operation = APIRouter(
    prefix = '/operation',
    tags   = ['operation'],
)


@operation.get('',
    status_code = 200,
    description = "Get all available operations.",
)
async def get_ops():
    return [
        name.split('.')[0]
        for name in listdir('data')
    ]


@operation.get('/{name}',
    status_code = 200,
    description = "Get operation by name.",
)
async def get_op(name: str):
    try:
        data = f'data/{name}.json'
        if Path(data).is_file():
            return load(open(data))
    except Exception as x:
        msg = f'\nGET OP ERR ! {x}\n'
        error(msg)
        raise HTTPException(
            status_code = 401,
            detail = msg,
        ) from x
    raise HTTPException(
        status_code = 404,
        detail = f'Operation not found : "{name}".',
    )


@operation.post('',
    status_code = 201,
    description = 'Add an operation',
)
async def add_op(data):
    try:
        full = f'data/{data["name"]}.json'
        with open(full, 'w') as out:
            dump(out, data)
    except Exception as x:
        raise HTTPException(
            status_code = 401,
            detail = 'Invalid operation data.',
        ) from x
