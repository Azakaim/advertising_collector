import asyncio

from settings import proj_settings
from src.clients.ozon_client import OzonClient
from src.pipelines.pipeline import run_pipeline
from src.services.google_sheet_service import GoogleSheetService


async def main() -> None:
    date_from = proj_settings.DATE_SINCE
    date_to = proj_settings.DATE_TO
    cli_ids = proj_settings.OZON_CLI_IDS.split(',')
    cli_secrets = proj_settings.OZON_CLI_SECRETS.split(',')
    lk_names = proj_settings.OZON_NAME_LK.split(',')
    # TODO доделать логику работы с сохранением адс в csv
    #PATH_TO_SAVE_CSV_FILES = proj_settings.PATH_TO_SAVE_CSV

    # google sheet
    google_sheet_titles = proj_settings.GOOGLE_SHEET_TITLES.split(',')
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    sheet_id = proj_settings.GOOGLE_SHEET_ID
    service_account_file_path = proj_settings.GOOLGLE_SERVICE_ACCOUNT_CREDS_PATH
    google_sheet = GoogleSheetService(scopes=scopes,
                                      path_creds=service_account_file_path,
                                      spreadsheet_id=sheet_id,
                                      titles=google_sheet_titles)
    ozon_cli = OzonClient(
        concurrency=20,
        default_rps=20,
        base_url=proj_settings.OZON_BASE_URL,
        ads_ids_url=proj_settings.OZON_ADS_IDS_URL,
        ads_companies_url=proj_settings.OZON_ADS_COMPANIES_URL,
        refresh_token_url=proj_settings.OZON_REFRESH_TOKEN_URL,
        statistics_status_url=proj_settings.OZON_STATISTICS_STATUSES_URL,
    )
    await run_pipeline(ozon_cli=ozon_cli, google_sheet=google_sheet,
                       cli_ids=cli_ids,cli_secrets=cli_secrets,lk_names=lk_names,
                       date_from=date_from,date_to=date_to)

if __name__ == '__main__':
    asyncio.run(main())
