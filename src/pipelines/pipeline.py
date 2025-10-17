import asyncio

from src.clients.ozon_bound_client import OzonCliBound
from src.clients.ozon_client import OzonClient
from src.pipelines.pipeline_steps import get_ads_analytics
from src.schemas.shemas import SellerAccount
from src.services.google_sheet_service import GoogleSheetService
from src.utils.utils_functions import extract_sellers, convert_to_sheet_values


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
                                        client_id=acc_creds.client_id,
                                        client_secret=acc_creds.client_secret,
                                        lk_name=acc_creds.name)
        for acc_creds in seller_accounts
    ]
    tasks = [get_ads_analytics(bcli, date_from, date_to,) for bcli in ozon_bound_clients]

    results = await asyncio.gather(*tasks)

    # TODO дописать логику записи в гугл таблицу
    values = await convert_to_sheet_values(date_from=date_from,
                                           date_to=date_to,
                                           ads_statistics=results,
                                           titles=google_sheet.titles)
    print(results)

    await google_sheet.push_to_google_sheet(values, "ADS_OZON")
    await google_sheet.format_google_sheet("A1:T1",
                                           "ADS_OZON",
                                           title_format=True)
