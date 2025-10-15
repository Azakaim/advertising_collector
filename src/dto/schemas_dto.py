from typing import NamedTuple

from pydantic import Field, dataclasses


class AdsOzonSchema(NamedTuple):
    avgBid: str
    campaign_id: str
    campaign_title: str
    clicks: str
    createdAt: str
    ctr: str
    drr: str
    modelsMoney: str
    moneySpent: str
    orders: str
    ordersMoney: str
    price: str
    search_query: str
    sku: str
    title: str
    toCart: str
    views: str

    @classmethod
    def convert(cls, data: dict) -> list["AdsOzonSchema"]:
        """
        Создаёт экземпляр AdsOzonSchema из словаря данных.
        Пропущенные поля заменяются на пустую строку.
        """
        result_ads = []
        for k, v in data.items():
            campaign_id = k
            campaign_title = v.get("title", "")
            for k2, v2 in v["report"].items():
                if k2 == "totals":
                    continue
                if len(v2) != 0:
                    for row in v2:
                        result_ads.append(cls(
                        avgBid=row.get("avgBid", ""),
                        campaign_id=campaign_id,
                        campaign_title=campaign_title,
                        clicks=row.get("clicks", ""),
                        createdAt=row.get("createdAt", ""),
                        ctr=row.get("ctr", ""),
                        drr=row.get("drr", ""),
                        modelsMoney=row.get("modelsMoney", ""),
                        moneySpent=row.get("moneySpent", ""),
                        orders=row.get("orders", ""),
                        ordersMoney=row.get("ordersMoney", ""),
                        price=row.get("price", ""),
                        search_query=row.get("search_query", ""),
                        sku=row.get("sku", ""),
                        title=row.get("title", ""),
                        toCart=row.get("toCart", ""),
                        views=row.get("views", "")
                ))
        return result_ads

@dataclasses.dataclass
class AdsRequest:
    attributionDays: str
    campaignId: str
    campaigns: list[str]
    dateFrom: str
    dateTo: str
    groupBy: str
    objects: list[object]
    date_to: str = Field(default="", alias="to")
    date_from: str = Field(default="", alias="from")

@dataclasses.dataclass
class AdsMeta:
    UUID: str
    createdAt: str
    kind: str
    request: AdsRequest
    state: str
    updatedAt: str
    error: str | None = None
    link: str | None = None

@dataclasses.dataclass
class AdsCampaign:
    id: str
    title: str

@dataclasses.dataclass
class AdsItem:
    campaigns: list[AdsCampaign]
    meta: AdsMeta
    name: str

@dataclasses.dataclass
class StatusUIDCollection:
    items: list[AdsItem]
    total: str
