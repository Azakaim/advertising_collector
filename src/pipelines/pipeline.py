import asyncio

from src.clients.ozon_bound_client import OzonCliBound
from src.clients.ozon_client import OzonClient
from src.dto.schemas_dto import AdsAnalytics
from src.pipelines.pipeline_steps import get_ads_analytics, get_ads_related_skus
from src.schemas.shemas import SellerAccount
from src.services.google_sheet_service import GoogleSheetService
from src.utils.utils_functions import extract_sellers, convert_to_sheet_values


async def run_pipeline(ozon_cli: OzonClient,
                       google_sheet: GoogleSheetService,
                       api_keys: list[str], 
                       lk_ids: list[str],
                       cli_ids: list[str],
                       cli_secrets: list[str],
                       lk_names: list[str],
                       date_from: str,
                       date_to: str) -> None:
    seller_accounts: list[SellerAccount] = extract_sellers(client_ads_ids=cli_ids,
                                                           client_secrets=cli_secrets,
                                                           lk_names=lk_names,
                                                           clients_seller_ids=lk_ids,
                                                           api_keys=api_keys)
    ozon_bound_clients = [ OzonCliBound(ozon_cli,
                                        client_ads_id=acc_creds.client_ads_id,
                                        client_seller_id=acc_creds.client_seller_id,
                                        client_secret=acc_creds.client_secret,
                                        lk_name=acc_creds.lk_name,
                                        api_key=acc_creds.api_key,
                                        )
        for acc_creds in seller_accounts
    ]
    ads_tasks = [get_ads_analytics(bcli, date_from, date_to,) for bcli in ozon_bound_clients]

    ads_results: list[AdsAnalytics] = await asyncio.gather(*ads_tasks) 
    
    # получаем связанные ску . здесь метод который отвечает за старые новые ску.
    # ads_related_skus_task = [get_ads_related_skus(blci, ads_i.reports) for blci, ads_i in zip(ozon_bound_clients, ads_results)]
    #
    # ads_related_skus = await asyncio.gather(*ads_related_skus_task)

    # для гугл таблицы значения
    values = await convert_to_sheet_values(date_from=date_from,
                                           date_to=date_to,
                                           ads_statistics=ads_results,
                                           titles=google_sheet.titles)

    await google_sheet.push_to_google_sheet(values, "ADS_OZON")
    await google_sheet.format_google_sheet("A1:T1",
                                           "ADS_OZON",
                                           title_format=True)
