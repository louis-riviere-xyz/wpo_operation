from os import environ


def _get(name, default):
    return environ.get(f'houses_{name}', default)


api_host      = _get('api_host', '0.0.0.0')
api_port      = _get('api_port', 8080)
app_secret    = _get('app_secret', 'supersecret')
