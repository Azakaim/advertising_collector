import asyncio

from settings import proj_settings
from src.clients.ozon_client import OzonClient
from src.pipelines.pipeline import run_pipeline


async def main() -> None:
    cli_ids = proj_settings.OZON_CLI_IDS.split(',')
    cli_secrets = proj_settings.OZON_CLI_SECRETS.split(',')
    ozon_cli = OzonClient(
        base_url=proj_settings.OZON_BASE_URL,
        ads_ids_url=proj_settings.OZON_ADS_IDS_URL,
        ads_companies_url=proj_settings.OZON_ADS_COMPANIES_URL,
        refresh_token_url=proj_settings.OZON_REFRESH_TOKEN_URL,
    )
    await run_pipeline(ozon_cli, cli_ids, cli_secrets)

if __name__ == '__main__':
    asyncio.run(main())
