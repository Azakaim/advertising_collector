from datetime import *
from itertools import chain
from zoneinfo import ZoneInfo

from src.dto.schemas_dto import StatusUIDCollection, AdsItem, AdsAnalytics
from src.infrastructure.cache import cache
from src.schemas.shemas import SellerAccount


def extract_sellers(client_ads_ids: list,
                    client_secrets: list,
                    lk_names: list,
                    clients_seller_ids: list[str],
                    api_keys: list[str]
                    ) -> list[SellerAccount]:
    """
    Extracts sellers from the environment variables.
    """
    if len(client_ads_ids) != len(client_secrets) != len(lk_names) != len(clients_seller_ids) != len(api_keys):
        raise ValueError("Client IDs, API keys, and names must have the same length.")

    return [
        SellerAccount(lk_name=lk_names[i],
                      client_secret=client_secrets[i],
                      client_ads_id=client_ads_ids[i],
                      client_seller_id=clients_seller_ids[i],
                      api_key=api_keys[i])

        for i in range(len(client_ads_ids))
    ]

async def get_converted_date_by_local(date_since, date_to):
    date_since = datetime.fromisoformat(f"{date_since}T00:00:00Z").astimezone(ZoneInfo("Asia/Yekaterinburg"))
    date_to = datetime.fromisoformat(f"{date_to}T23:59:59Z").astimezone(ZoneInfo("Asia/Yekaterinburg"))
    print(date_since.strftime("%Y-%m-%dT%H:%M:%S"), date_to.strftime("%Y-%m-%dT%H:%M:%S"))
    return date_since.strftime("%Y-%m-%dT%H:%M:%S") + "Z", date_to.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

async def get_success_statuses_ads_ids(success_statuses: StatusUIDCollection) -> list[AdsItem]:
    items = [si for si in success_statuses.items if si.meta.error is None]
    return items

async def get_sorted_ads_ids(success_ads_ids: list[AdsItem] | list[str], ads_ids: list, date_from: date, date_to: date):
    last_version_ads_stats_by_id = {}
    # переворачиваем список если вдруг найдем одинаковые айдишники с успешным статусом
    # проверив все id получим последний актуальный те первое вхождение
    common_ads_stats = set()
    if not all(isinstance(_id, str) for _id in success_ads_ids) :
        common_ads_stats = set(chain.from_iterable([[c.id for c in cas.campaigns] for cas in success_ads_ids]))
    for sai in success_ads_ids[::-1]:
        if hasattr(sai,"campaigns"):
            for _id in sai.campaigns:
                if _id.id not in common_ads_stats:#batch:
                    last_version_ads_stats_by_id.update({_id.id: ""})
                else:
                    if (sai.meta.request.date_from != str(date_from)
                            and sai.meta.request.date_to != str(date_to)) or sai.meta.link is None:
                        last_version_ads_stats_by_id.update({_id.id: sai.meta.state})
                    else:
                        # TODO доделать случай если и айдишник есть и дата совпадает ,мысль такая что если совпааде тто вернуть последний обьект уид типа для получения
                        last_version_ads_stats_by_id[_id.id] = sai.meta.link
        else:
            last_version_ads_stats_by_id.update({sai: ""})
    if len(last_version_ads_stats_by_id.keys()) != len(ads_ids):
        l_diff = ads_ids - last_version_ads_stats_by_id.keys()
        last_version_ads_stats_by_id.update({_id: "" for _id in l_diff})
    changed_id_by_link = await reverse_key_value(last_version_ads_stats_by_id)
    return changed_id_by_link

async def convert_to_sheet_values(date_from: str, date_to: str, ads_statistics: list[AdsAnalytics], titles: list[str]) :
    # объявляем заголовки
    values = [titles]
    for ads_reports in ads_statistics:
        if len(ads_reports.reports) > 0:
            for ads in ads_reports.reports:
                value = [ads_reports.lk_name , ads.sku, ads.title, ads.campaign_id, ads.campaign_title,
                         f"{date_from}:{date_to}", ads.createdAt, ads.avgBid, ads.views,
                         ads.clicks, ads.ctr, ads.toCart, ads.orders, ads.ordersMoney,
                         ads.price, ads.moneySpent, ads.modelsMoney, "-----", ads.drr, ads.search_query]
                values.append(value)
    return values

async def flatten_list(nested_l: list) -> list:
    flattened = []
    for i in nested_l:
        if isinstance(i, list):
            flattened.extend(await flatten_list(i))
        else:
            flattened.append(i)
    return flattened

async def reverse_key_value(dictionary: dict) -> dict:
    new_dict:dict[str, list] = {}
    for key, value in dictionary.items():
        if value not in new_dict:
            new_dict[value] = [key]
        else:
            new_dict[value].append(key)
    return new_dict

async def make_cache(key, data):
    cache.set(key, data.model_dump_json(), ex=86400)
    return True

async def get_cache(key):
    return cache.get(key)
