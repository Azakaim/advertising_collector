from src.clients.ozon_bound_client import OzonCliBound
from src.clients.ozon_client import OzonClient
from src.clients.services import OzonService


async def run_pipeline(ozon_cli: OzonClient,
                       cli_ids: list,
                       cli_secrets: list[str],
                       date_from: str,
                       date_to: str) -> None:
    ozone_bound = OzonCliBound(ozon_cli,
                               client_id=cli_ids[0],
                               client_secret=cli_secrets[0])

    ozon_service = OzonService(cli=ozone_bound)
    # получить ids рекламы
    ads_ids = await ozon_service.get_advertising_ids()
    # получить рекламные компании на кабинете
    co = await ozon_service.get_advertising_companies_by_acc(ads_ids=ads_ids,
                                                             date_from=date_from,
                                                             date_to=date_to)


    print(co)
    print(co)
