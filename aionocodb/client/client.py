from aiohttp.client import ClientSession
from aiohttp.client import ClientTimeout

from .models import JWTAuthToken
from .models import APIToken

from .table_row import TableRow

from typing import Union

        

class Client():
    def __init__(self,
                 host: str,
                 token: Union[APIToken, JWTAuthToken]
                 ):
        self.host=host
        self.token=token
        self.headers=self.token.get_header()
        self.headers.update({"Content-Type": "application/json"})
        self.session=Client.get_session(self)
        
        self.table_row = TableRow(
            host=self.host,
            token=self.token,
            headers=self.headers,
            session=self.session
        )


    def get_session(self):
        return ClientSession(
            headers=self.headers,
            timeout=ClientTimeout(total=5),

        )


    async def __aenter__(self):
        self.session=Client.get_session(self)
        return self


    async def __aexit__(self, exc_type, exc, tb):
        await self.table_row.session.close()
        await self.storage.session.close()
        await self.session.close()