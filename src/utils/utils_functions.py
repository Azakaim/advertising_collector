from datetime import *
from zoneinfo import ZoneInfo

from src.dto.schemas_dto import StatusUIDCollection, AdsItem
from src.schemas.shemas import SellerAccount


def extract_sellers(client_ids: list,
                    api_keys: list,
                    names: list) -> list[SellerAccount]:
    """
    Extracts sellers from the environment variables.
    """
    if len(client_ids) != len(api_keys) != len(names):
        raise ValueError("Client IDs, API keys, and names must have the same length.")

    return [
        SellerAccount(api_key=api_keys[i], name=names[i], client_id=client_ids[i])
        for i in range(len(client_ids))
    ]

async def get_converted_date_by_local(date_since, date_to):
    date_since = datetime.fromisoformat(f"{date_since}T00:00:00Z").astimezone(ZoneInfo("Asia/Yekaterinburg"))
    date_to = datetime.fromisoformat(f"{date_to}T23:59:59Z").astimezone(ZoneInfo("Asia/Yekaterinburg"))
    print(date_since.strftime("%Y-%m-%dT%H:%M:%S"), date_to.strftime("%Y-%m-%dT%H:%M:%S"))
    return date_since.strftime("%Y-%m-%dT%H:%M:%S") + "Z", date_to.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

async def get_success_statuses_ads_ids(success_statuses: StatusUIDCollection) -> list[AdsItem]:
    items = [si for si in success_statuses.items if si.meta.state == "OK"]
    return items
