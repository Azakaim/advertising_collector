from typing import Optional

from pydantic import BaseModel, Field


class AutoIncrease(BaseModel):
    autoIncreasePercent: Optional[int] = Field(default=int, alias="auto_increase_percent")
    autoIncreasedBudget: Optional[int] = Field(default=int, alias="auto_increased_budget")
    isAutoIncreased: Optional[bool] = Field(default=False, alias="is_auto_increased")
    recommendedAutoIncreasePercent: Optional[int] = Field(default=int, alias="recommended_auto_increase_percent")

    model_config = {
        "populate_by_name": True ,
        "arbitrary_types_allowed": True
    }

class AdsCompanies(BaseModel):
    id: Optional[int] = Field(default=int)
    paymentType: Optional[str] = Field(default_factory=str,alias="payment_type")
    title: Optional[str] = Field(default_factory=str)
    state: Optional[str] = Field(default_factory=str)
    advObjectType: Optional[str] = Field(default_factory=str,alias="advobject_type")
    fromDate: Optional[str] = Field(default_factory=str,alias="from_date")
    toDate: Optional[str] = Field(default_factory=str,alias="to_date")
    dailyBudget: Optional[int] = Field(default=int, alias="daily_budget")
    placement: Optional[list[str]] = Field(default_factory=list)
    budget: Optional[int] = Field(default=int)
    createdAt: Optional[str] = Field(default_factory=str,alias="created_at")
    updatedAt: Optional[str] = Field(default_factory=str,alias="updated_at")
    productAutopilotStrategy: Optional[str] = Field(default_factory=str,alias="product_autopilot_strategy")
    productCampaignMode: Optional[str] = Field(default_factory=str,alias="product_campaign_mode")
    autoIncrease: Optional[AutoIncrease] = Field(default_factory=AutoIncrease,alias="auto_increase")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class CollectionAdsCompanies(BaseModel):
    ads_list: list[AdsCompanies] = Field(default_factory=list, alias='list')

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class SellerAccount(BaseModel):
    """
    Ozon_cli API settings.
    """
    api_key: str = Field(..., description="API key for Ozon API")
    name: str = Field(..., description="Name of the seller in Ozon")
    client_id: str = Field(..., description="Client ID for Ozon API")

class RequestBodyAdsCompanies(BaseModel):
    campaigns: list[str]
    d_from: str = Field(default='', alias='from')
    d_to: str = Field(default='', alias='to')
    date_from: str = Field(default='', alias='dateFrom')
    date_to: str = Field(default='', alias='dateTo')
    group_by: str = Field(default='DATE', alias='groupBy')

    model_config = {
            "populate_by_name": True
        }
