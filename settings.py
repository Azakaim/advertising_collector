from dotenv import load_dotenv
from environs import Env
from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):

    REDIS_HOST: str = Field("", env="REDIS_HOST")
    REDIS_PORT: str = Field("", env="REDIS_PORT")
    #
    # GOOGLE_SPREADSHEET_ID: str = Field("", env="GOOGLE_SPREADSHEET_ID")
    # GOOGLE_CLIENT_SECRET: str = Field("", env="GOOGLE_CLIENT_SECRET")
    # GOOGLE_SHEETS_URI: str = Field("", env="GOOGLE_SHEETS_URI")
    # SERVICE_SCOPES: str = Field("", env="SCOPES")
    # PATH_TO_CREDENTIALS: str = Field("", env="PATH_TO_CREDENTIALS")
    # GOOGLE_BASE_TOP_SHEET_TITLES: str = Field("", env="GOOGLE_SHEET_BASE_TITLES")
    # GOOGLE_BASE_SHEETS_TITLES_BY_ACC: str = Field("", env="GOOGLE_BASE_SHEETS_TITLES_BY_ACC")

    PATH_TO_SAVE_CSV: str = Field("", env="OZON_BASE_URL")

    GOOGLE_SHEET_ID: str = Field("", env="GOOGLE_SHEET_ID")
    GOOLGLE_SERVICE_ACCOUNT_CREDS_PATH: str = Field("", env="GOOLGLE_SERVICE_ACCOUNT_CREDS_PATH")
    GOOGLE_SHEET_TITLES: str = Field("", env="GOOGLE_SHEET_TITLES")

    OZON_STATISTICS_REPORT_URL: str = Field("", env="OZON_STATISTICS_REPORT_URL")
    OZON_BASE_URL: str = Field("", env="OZON_BASE_URL")
    OZON_NAME_LK: str = Field("", env="OZON_NAME_LK")
    OZON_CLI_IDS: str = Field("", env="OZON_CLI_IDS")
    OZON_CLI_SECRETS: str = Field("", env="OZON_CLI_SECRETS")
    OZON_REFRESH_TOKEN_URL: str = Field("", env="OZON_REFRESH_TOKEN_URL")
    OZON_ADS_IDS_URL: str = Field("",env="OZON_ADS_IDS_URL")
    OZON_ADS_COMPANIES_URL: str = Field("",env="OZON_ADS_COMPANIES_URL")
    OZON_STATISTICS_STATUSES_URL: str = Field("", env="OZON_STATISTICS_STATUSES_URL")
    DATE_SINCE: str = Field("", env="DATE_SINCE")
    DATE_TO: str = Field("", env="DATE_TO")

    BUCKET_NAME: str = Field("", env="BUCKET_NAME")
    S3_ACCESS_KEY: str = Field("", env="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field("", env="S3_SECRET_KEY")
    S3_ENDPOINT: str = Field("", env="S3_ENDPOINT")

    class Config:
        env = Env()
        load_dotenv()
        env.read_env()

proj_settings = Settings()
