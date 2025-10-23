import asyncio

from src.clients.ozon_bound_client import OzonCliBound
from src.dto.schemas_dto import AdsOzonSchema, AdsAnalytics
from src.services.ozon_services import OzonService
from src.utils.utils_functions import get_converted_date_by_local, get_success_statuses_ads_ids, get_sorted_ads_ids, \
    flatten_list


async def get_ads_analytics(ozone_bound: OzonCliBound,
                            date_from: str,
                            date_to: str):
    # собираем uids запущенных в сбор по аналитике рекл компаний
    uid = None

    ozon_service = OzonService(cli=ozone_bound)
    # конвертировать в дату с часовым поясом
    date_since, date_till = await get_converted_date_by_local(date_from, date_to)
    # получить ids рекламы
    ads_ids = await ozon_service.get_advertising_ids()
    # уточняем есть ли уже готовые отчеты
    status_reports = await ozon_service.get_statistics_statuses()
    # если отчеты есть проверяем статусы
    ads_ids_by_statuses = await get_success_statuses_ads_ids(status_reports)
    # отсортировать id рекламных компаний со статусами ОК, взять только те по которым мы еще не делали запрос на статистику
    link_by_ads_ids = await get_sorted_ads_ids(success_ads_ids=ads_ids_by_statuses
                                                if int(status_reports.total) != 0  else ads_ids,  # если статусов нет то берем ads_ids,
                                               ads_ids=ads_ids,
                                               date_from=date_since,
                                               date_to=date_till)
    # собираем отчеты
    reports: list[AdsOzonSchema] = []
    for link in link_by_ads_ids:
        # важно если в рекламе за указанную дату не было метрик результат None
        if link and (link != "NOT_STARTED"):
            report = await ozon_service.get_report(link)
            if report is not None:
                reports.extend(report)
    # отправить запрос на получение инфы о рекл
    ids_without_links = link_by_ads_ids.get("")
    if ids_without_links:
        sorted_ads_ids = await flatten_list(link_by_ads_ids.get(""))
        uid = await ozon_service.get_advertising_companies_stats(ads_ids=sorted_ads_ids,
                                                                  date_from=date_since,
                                                                  date_to=date_till)

    return AdsAnalytics(uid=uid,reports=reports,lk_name=ozone_bound.lk_name)

async def get_ads_related_skus(ozone_bound: OzonCliBound, data: list[AdsOzonSchema]):
    oz_service = OzonService(cli=ozone_bound)
    tasks = [oz_service.get_related_skus(sku=d.sku) for d in data]
    related_skus = await asyncio.gather(*tasks)

    return ozone_bound.lk_name ,related_skus