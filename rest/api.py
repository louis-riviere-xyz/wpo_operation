from logging import error

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from .routes import routes
from . import title, description, version


api = FastAPI()

vld = False
chk = False


@api.exception_handler(RequestValidationError)
async def valid_excep_handler(req, exc):
    vld and error(f"call : {req.scope['method']} {req.scope['path']}")
    vld and error(f'exc  : {exc}')
    vld and error(f'body : {exc.body}')
    return PlainTextResponse(str(exc), status_code=444)


@api.middleware("http")
async def check(request, call_next):
    chk and error(f'  --> {vars(request)}')
    chk and error(f'  --> {request.scope}')
    response = await call_next(request)
    chk and error(f' <--  {response.status_code}')
    return response


for route in routes:
    api.include_router(route)


api.openapi_schema = get_openapi(
    title       = title,
    description = description,
    version     = version,
    routes      = api.routes,
)
