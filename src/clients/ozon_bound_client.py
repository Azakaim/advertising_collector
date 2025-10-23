import logging
from typing import Optional, Any

from src.clients.ozon_client import OzonClient
from src.schemas.shemas import RequestBodyAdsCompanies

log = logging.getLogger("ozon bound client")

class OzonCliBound:
    def __init__(self, base: OzonClient,
                 client_ads_id: str,
                 client_seller_id: str,
                 client_secret: str,
                 lk_name: str,
                 api_key: str) -> None:
        self.lk_name = lk_name
        self._base = base
        self.addition_headers = {
            "Client-Id": client_seller_id,
            "Api-Key": api_key,
            "Content-Type": "application/json",
        }
        self.pyload_refr_token = {
            "client_id": client_ads_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        self._headers: dict[str, str] = {
            "Host": "api-performance.ozon.ru:443",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self._jwt: Optional[str] = None

    @property
    def headers(self) -> dict[str, str]:
        headers = self._headers.copy()
        if self._jwt:
            headers["Authorization"] = f"Bearer {self._jwt}"
        return headers

    @headers.setter
    def headers(self, value: dict[str, str]):
        self._headers = value

    async def _parse_jwt(self, body) -> tuple[str | None, int | None]:
        if 'expires_in' and 'access_token' in body:
            jwt = body['access_token']
            expires_in = body['expires_in']
            return (jwt,
                    expires_in) # TODO реализовать логику подсчета истечения времени токена
        return None, None

    async def refresh_token(self) -> Optional[Any]:
            """Обёртка, автоматически добавляющая заголовки и токен"""

            req = await self.request("POST",
                                     self._base.refresh_token_url,
                                     json=self.pyload_refr_token)
            self._jwt, sec = await self._parse_jwt(req)
            print(self.headers)

    async def fetch_advertising_ids(self) -> Optional[Any]:
        await self.refresh_token()
        return await self._base.fetch_advertising_ids(headers=self.headers)

    async def fetch_related_skus(self, sku: dict[str, list[str]]) -> Optional[Any]:
        return await self._base.fetch_related_skus(sku=sku, headers=self.addition_headers)

    async def fetch_stats_report(self, link: str) -> Optional[Any]:
        return await self._base.fetch_stats_report(link, headers=self.headers)

    async def fetch_advertising_company_statistics(self, data: RequestBodyAdsCompanies) -> Optional[Any]:
        return await self._base.fetch_advertising_company_statistics(data, headers=self.headers)

    async def fetch_statistics_statuses(self) -> Optional[Any]:
        return await self._base.fetch_statistics_statuses(headers=self.headers)

    async def request(self, method: str, endpoint: str, *, json: Optional[dict]=None):
        return await self._base.request(method, endpoint, json=json, headers=self.headers)

    async def aclose(self):
        await self._base.aclose()
