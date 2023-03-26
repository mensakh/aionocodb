from ..helpers import Helpers

from aiohttp import ClientSession


class Storage:
    def __init__(self, host, token, headers, session):
        self.host = host
        self.token = token
        self.headers = headers
        self.session = session
        self.session: ClientSession