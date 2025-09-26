import logging

from typing import Dict, Optional, Any

from pydantic import PrivateAttr

from src.schemas.shemas import RequestBodyAdsCompanies
from src.utils.http_base_client import BaseRateLimitedHttpClient
from src.utils.limiter import RateLimiter


log = logging.getLogger("ozon client")

class OzonClient(BaseRateLimitedHttpClient):
    base_url: str
    ads_ids_url: str
    ads_companies_url: str
    refresh_token_url: str
    statistics_status_url: str

    _per_endpoint_rps: Optional[Dict[str, int]] = PrivateAttr(default_factory=dict) # например: {"/v2/product/info": 5}

    def model_post_init(self, __context):
        super().model_post_init(__context)
        # self._per_endpoint_rps[self.analytics_url] = 1
        # инициализируем лимитеры для каждого эндпоинта #TODO: убрать, если не нужен лимиттер для каждого эндпоинта
        if self._per_endpoint_rps:
            for ep, rps in self._per_endpoint_rps.items():
                self._limiters[ep] = RateLimiter(rps, 60.0)

    async def fetch_advertising_ids(self, headers: dict) -> Optional[Any]:
        return await self.request("GET", self.ads_ids_url, headers=headers)

    async def fetch_advertising_company_statistics(self, data: RequestBodyAdsCompanies, headers: dict) -> Optional[Any]:
        return await self.request("POST", self.ads_companies_url, json=data.model_dump(), headers=headers)

    async def fetch_statistics_status(self,uid: str, headers: dict) -> Optional[Any]:
        return await self.request("GET", self.statistics_status_url + uid, headers=headers)
