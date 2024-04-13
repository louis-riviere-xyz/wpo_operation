from uvicorn import run

from rest.api import api
from .config import api_host, api_port


def main():
    run(api,
        host       = api_host,
        port       = api_port,
        use_colors = False,
    )


if __name__ == '__main__': main()
