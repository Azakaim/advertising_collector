import asyncio

from src.clients.ozon_bound_client import OzonCliBound
from src.clients.ozon_client import OzonClient
from src.pipelines.pipeline_steps import get_ads_analytics
from src.schemas.shemas import SellerAccount
from src.services.google_sheet_service import GoogleSheetService
from src.utils.utils_functions import extract_sellers


async def run_pipeline(ozon_cli: OzonClient,
                       google_sheet: GoogleSheetService,
                       cli_ids: list[str],
                       cli_secrets: list[str],
                       lk_names: list[str],
                       date_from: str,
                       date_to: str) -> None:
    seller_accounts: list[SellerAccount] = extract_sellers(client_ids=cli_ids,
                                                           client_secrets=cli_secrets,
                                                           names=lk_names)
    ozon_bound_clients = [ OzonCliBound(ozon_cli,
                                        client_id=bcli.client_id,
                                        client_secret=bcli.client_secret)
        for bcli in seller_accounts
    ]
    tasks = [get_ads_analytics(bcli, date_from, date_to) for bcli in ozon_bound_clients]

    results = await asyncio.gather(*tasks)

    # TODO дописать логику записи в гугл таблицу
    google_sheet.create_values_to_google_sheet()
    print(results)
    # ozone_bound = OzonCliBound(ozon_cli,
    #                            client_id=cli_ids[0],
    #                            client_secret=cli_secrets[0])
    #
    # ozon_service = OzonService(cli=ozone_bound)
    # # конвертировать в дату с часовым поясом
    # date_since, date_till = await get_converted_date_by_local(date_from, date_to)
    # # получить ids рекламы
    # ads_ids = await ozon_service.get_advertising_ids()
    # # уточняем есть ли уже готовые отчеты
    # status_reports = await ozon_service.get_statistics_statuses()
    # # если отчеты есть проверяем статусы
    # ads_ids_by_statuses = await get_success_statuses_ads_ids(status_reports) \
    #                         if status_reports else ads_ids # если статусов нет то берем ads_ids
    # # отсортировать id рекламных компаний со статусами ОК, взять только те по которым мы еще не делали запрос на статистику
    # link_by_ads_ids = await get_sorted_ads_ids(success_ads_ids=ads_ids_by_statuses,
    #                                            ads_ids=ads_ids,
    #                                            date_from=date_since,
    #                                            date_to=date_till)
    # # собираем отчеты
    # reports = []
    # status = link_by_ads_ids.keys()
    # for link in link_by_ads_ids :
    #     # важно если в рекламе за указанную дату не было метрик результат None
    #     if link and (link != "NOT_STARTED"):
    #         report = await ozon_service.get_report(link)
    #         if report is not None:
    #             reports.extend(report)
    # # отправить запрос на получение инфы о рекл
    # ids_without_links = link_by_ads_ids.get("")
    # sorted_ads_ids = None
    # if ids_without_links:
    #     sorted_ads_ids = await flatten_list(link_by_ads_ids.get(""))
    #     uids = await ozon_service.get_advertising_companies_stats(ads_ids=sorted_ads_ids,
    #                                                               date_from=date_since,
    #                                                               date_to=date_till)
    # print(f"Обновлять нечего, статус для {ads_ids} : {status}")
    # TODO дописать логику для работы если уид получили то коллектим со всех кабинетов
    # if uids:
    #
    # TODO затем все это закидываем в гугл таблицу
