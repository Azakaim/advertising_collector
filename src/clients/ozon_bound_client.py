import logging
from typing import Optional

from src.clients.ozon_client import OzonClient

log = logging.getLogger("ozon bound client")

class OzonCliBound:
    def __init__(self, base: OzonClient,
                 headers: dict[str,str]):
                 self._base = base
                 self._headers = headers

    async def request(self, method: str, endpoint: str, *, json: Optional[dict]=None):
        return await self._base.request(method, endpoint, json=json, headers=self._headers)

    async def aclose(self):
        await self._base.aclose()
