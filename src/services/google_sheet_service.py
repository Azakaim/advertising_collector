from typing import Any

import gspread
from google.oauth2.service_account import Credentials
from gspread import Spreadsheet
from pydantic import BaseModel, Field

from src.dto.schemas_dto import AdsOzonSchema


class GoogleSheetService(BaseModel):
    scopes: list[str] = Field(default_factory=list)
    path_creds: str = Field(default_factory=str)
    spreadsheet_id: str = Field(default_factory=str)
    sheet: Spreadsheet = Field(default=None)
    titles: list[str] = Field(default_factory=list)

    model_config = {
        "arbitrary_types_allowed" :True
    }

    def model_post_init(self,__context):
        try:
            # Указываем scope и путь к ключу сервисного аккаунта
            creds = Credentials.from_service_account_file(self.path_creds, scopes=self.scopes)
            # Авторизация
            gc = gspread.authorize(creds)
            # Открываем таблицу по ID
            self.sheet = gc.open_by_key(self.spreadsheet_id)
            # sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlmNoPqRstuVwXyZ1234567890/edit#gid=0")
        except Exception as e:
            raise Exception(e)

    def create_values_to_google_sheet(self, titles: list[str], values: list[Any]) -> list:
        return titles + values

    async def convert_to_sheet_values(self, lk_name: str, ads_statistics: list[AdsOzonSchema]):
        values = []
        for ads in ads_statistics:
            # TODO дописать конверт
            value = [lk_name , ads.sku, ads.title, ads.campaign_id, ads.campaign_title, ads.]
        ...

    def push_to_google_sheet(self,data: list, sheet_name: str) -> None:
        # Выбираем лист
        worksheet = self.sheet.worksheet(sheet_name)

        # Записываем данные
        worksheet.update(data,"A1")

    def format_google_sheet(self,sh_range: str, sheet_name: str, title_format: bool = False) -> None:
        # Выбираем лист
        worksheet = self.sheet.worksheet(sheet_name)
        worksheet.format(sh_range, {
            "backgroundColor": {"red":0.90, "green": 0.9, "blue": 0.0}
        })
        if title_format:
            worksheet.format(sh_range, {
                             "textFormat": {"bold": True, "italic": True, "fontSize": 12},
                             "horizontalAlignment": "CENTER",
                             "verticalAlignment": "MIDDLE"
            })
