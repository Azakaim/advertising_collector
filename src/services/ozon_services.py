import asyncio
from typing import Any
from itertools import batched

from pydantic import BaseModel

from src.clients.ozon_bound_client import OzonCliBound
from src.dto.schemas_dto import StatusUIDCollection, AdsOzonSchema
from src.schemas.shemas import CollectionAdsCompanies, RequestBodyAdsCompanies
from src.utils.http_base_client import APIError


class OzonService(BaseModel):
    cli: OzonCliBound

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

    async def get_advertising_ids(self) -> Any:
        ads_data = await self.cli.fetch_advertising_ids()
        parsed_ids = CollectionAdsCompanies(**ads_data)
        return [str(ids.id) for ids in parsed_ids.ads_list]

    async def get_statistics_statuses(self) -> Any:
        statuses = await self.cli.fetch_statistics_statuses()
        return StatusUIDCollection(**statuses)

    async def get_advertising_companies_stats(self, ads_ids: list[int], date_from: str, date_to: str):
        """
        :param ads_ids: list
        :param date_from: str format 2000-12-31
        :param date_to: str format 2000-12-31
        :return: uids of companies stats
        """
        for batch in batched(ads_ids, 10):
            body = RequestBodyAdsCompanies(
                campaigns=[str(x) for x in list(batch)],
                d_from=date_from,
                d_to=date_to,
                group_by="NO_GROUP_BY"
            )
            ads_co = await self.cli.fetch_advertising_company_statistics(data=body)
            if isinstance(ads_co, APIError):
                return None
            # тк метод асинхронный он не принимает более одной партии айдишек поэтому выходим из цикла до получения отчета
            return ads_co["UUID"]
        return None

    async def get_report(self, prepared_stats_link):
        ads_results =  await self.cli.fetch_stats_report(prepared_stats_link)
        return AdsOzonSchema.convert(ads_results)

    async def get_related_skus(self, sku: str):
        related_skus= await self.cli.fetch_related_skus(sku={"sku": [sku]})
        return sku, related_skus
