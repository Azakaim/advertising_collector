from src.clients.ozon_bound_client import OzonCliBound
from src.clients.ozon_client import OzonClient
from src.clients.services import OzonService
from src.dto.schemas_dto import StatusUIDCollection
from src.utils.utils_functions import get_converted_date_by_local, get_success_statuses_ads_ids


async def run_pipeline(ozon_cli: OzonClient,
                       cli_ids: list,
                       cli_secrets: list[str],
                       date_from: str,
                       date_to: str) -> None:
    ozone_bound = OzonCliBound(ozon_cli,
                               client_id=cli_ids[0],
                               client_secret=cli_secrets[0])

    ozon_service = OzonService(cli=ozone_bound)
    # уточняем есть ли уже готовые отчеты
    status_reports = await ozon_service.get_statistics_statuses()
    # если отчеты есть проверяем статусы
    success_statuses_ads_ids = await get_success_statuses_ads_ids(status_reports) if status_reports else None
    # собираем отчеты
    r = []
    for ads_item in success_statuses_ads_ids:
        r.extend(await ozon_service.get_report(ads_item.meta.link))
    # получить ids рекламы
    ads_ids = await ozon_service.get_advertising_ids()
    # конвертировать в дату с часовым поясом
    date_since, date_till = await get_converted_date_by_local(date_from, date_to)
    # отправить запрос на получение инфы о рекл
    uids = await ozon_service.get_advertising_companies_stats(ads_ids=ads_ids,
                                                              date_from=date_since,
                                                              date_to=date_till)
    if uids:
        #TODO дописать логику для работы если уид получили
        ...
