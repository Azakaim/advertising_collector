from typing import Any
from itertools import batched

from pydantic import BaseModel

from src.clients.ozon_bound_client import OzonCliBound
from src.schemas.shemas import CollectionAdsCompanies, RequestBodyAdsCompanies


class OzonService(BaseModel):
    cli: OzonCliBound

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

    async def get_advertising_ids(self) -> Any:
        ads_data = await self.cli.fetch_advertising_ids()
        parsed_ids = CollectionAdsCompanies(**ads_data)
        return [ids.id for ids in parsed_ids.ads_list]

    async def get_statistics_status(self, uid: str) -> Any:
        req = self.cli.fetch_statistics_status(uid)

    async def get_advertising_companies_by_acc(self, ads_ids: list[int], date_from: str, date_to: str) -> Any:
        """

        :param ads_ids: list
        :param date_from: str format 2000-12-31
        :param date_to: str format 2000-12-31
        :return:
        """
        result = []
        count = 0
        for batch in batched(ads_ids, 1):
            if count == 0:
                count+=1
                continue
            list(batch)
            body = RequestBodyAdsCompanies(d_to='',d_from='',
                date_from=date_from,
                date_to=date_to,
                campaigns=[str(x) for x in list(batch)],
            )
            ads_co = await self.cli.fetch_advertising_company_statistics(data=body)
            uid = ads_co

            result.extend(ads_co)

        print(result)
