from pydantic import BaseModel, Field


class AutoIncrease(BaseModel):
    autoIncreasePercent: int = Field(default=int, alias="auto_increase_percent")
    autoIncreasedBudget: int = Field(default=int, alias="auto_increased_budget")
    isAutoIncreased: bool = Field(default=False, alias="is_auto_increased")
    recommendedAutoIncreasePercent: int = Field(default=int, alias="recommended_auto_increase_percent")

    model_config = {
        "populate_by_name": True ,
        "arbitrary_types_allowed": True
    }

class AdsCompanies(BaseModel):
    id: int = Field(default=int)
    paymentType: str = Field(default_factory=str,alias="payment_type")
    title: str = Field(default_factory=str)
    state: str = Field(default_factory=str)
    advObjectType: str = Field(default_factory=str,alias="advobject_type")
    fromDate: str = Field(default_factory=str,alias="from_date")
    toDate: str = Field(default_factory=str,alias="to_date")
    dailyBudget: int = Field(default=int, alias="daily_budget")
    placement: list[str] = Field(default_factory=list)
    budget: int = Field(default=int)
    createdAt: str = Field(default_factory=str,alias="created_at")
    updatedAt: str = Field(default_factory=str,alias="updated_at")
    productAutopilotStrategy: str = Field(default_factory=str,alias="product_autopilot_strategy")
    productCampaignMode: str = Field(default_factory=str,alias="product_campaign_mode")
    autoIncrease: AutoIncrease = Field(default_factory=AutoIncrease,alias="auto_increase")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class Root(BaseModel):
    list: AdsCompanies = Field(default_factory=AdsCompanies)

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
