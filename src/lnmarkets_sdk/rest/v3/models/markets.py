from typing import Literal

from pydantic import BaseModel, Field, SkipValidation

from lnmarkets_sdk.rest.v3._internal.models import BaseConfig

MarketInstrument = Literal["inverse_perp", "quanto_perp", "quanto_spot"]
MarketStatus = Literal["hidden", "early_access:closed", "early_access:open", "released"]


class MarketCrossLimits(BaseModel, BaseConfig):
    """Cross margin limits of a perp market."""

    max_order_count: SkipValidation[int]
    max_order_quantity: SkipValidation[float]
    max_quantity_at_min_leverage: SkipValidation[float]
    max_quantity_at_max_leverage: SkipValidation[float]


class MarketLimits(BaseModel, BaseConfig):
    """Trading limits of a market."""

    max_trade_count: SkipValidation[int]
    max_order_quantity: SkipValidation[float]
    max_account_quantity: SkipValidation[float]
    cross: MarketCrossLimits | None = Field(
        default=None, description="Cross margin limits (perp markets only)"
    )


class Market(BaseModel, BaseConfig):
    """A market available to the caller."""

    id: SkipValidation[str] = Field(..., description="Market id, `<instrument>:<pair>`")
    instrument: SkipValidation[MarketInstrument]
    pair: SkipValidation[str] = Field(..., description="Pair of the market")
    slug: SkipValidation[str]
    symbol: SkipValidation[str]
    ticker: SkipValidation[str]
    display_name: SkipValidation[str]
    base_asset: SkipValidation[str]
    quote_asset: SkipValidation[str]
    tick_size: SkipValidation[float] = Field(..., description="Price increment")
    quantity_step: SkipValidation[float] = Field(..., description="Quantity increment")
    quantity_unit: SkipValidation[Literal["btc", "usd", "oz", "bbl", "share"]]
    limits: MarketLimits
    status: SkipValidation[MarketStatus]
    feature: SkipValidation[str] | None = None
    funding_interval_hours: SkipValidation[int] | None = Field(
        default=None, description="Hours between funding settlements (perp only)"
    )
    max_leverage: SkipValidation[int] | None = Field(
        default=None, description="Maximum leverage (perp only)"
    )
    margin_modes: SkipValidation[list[Literal["isolated", "cross"]]] | None = Field(
        default=None, description="Supported margin modes (perp only)"
    )
