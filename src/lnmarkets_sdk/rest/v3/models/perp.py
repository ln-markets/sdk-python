# Pydantic discriminated-union pattern intentionally narrows base-class fields
# in concrete trade variants (see futures_isolated.py).
# pyright: reportIncompatibleVariableOverride=false

from typing import Literal

from pydantic import BaseModel, Field, SkipValidation, model_validator

from lnmarkets_sdk.rest.v3._internal.models import UUID, BaseConfig
from lnmarkets_sdk.rest.v3.models.futures_data import (
    Candle,
    CandleResolution,
    PriceBucket,
    PriceChange24h,
)
from lnmarkets_sdk.rest.v3.models.futures_isolated import (
    FuturesCanceledTrade,
    FuturesClosedTrade,
    FuturesOpenTrade,
    FuturesRunningTrade,
)

PerpInstrument = Literal["inverse_perp", "quanto_perp"]


class PerpMarketKey(BaseModel, BaseConfig):
    """Market key of a perp market, e.g. `inverse_perp` + `btc_usd`."""

    instrument: PerpInstrument = Field(..., description="Instrument of the market")
    pair: str = Field(..., description="Pair of the market, e.g. 'btc_usd'")


class PerpMarketFilter(BaseModel, BaseConfig):
    """Optional market key: both fields select one market, none selects all."""

    instrument: PerpInstrument | None = Field(
        default=None, description="Instrument of the market"
    )
    pair: str | None = Field(default=None, description="Pair of the market")

    @model_validator(mode="after")
    def validate_market_key(self):
        if (self.instrument is None) != (self.pair is None):
            raise ValueError("Pass both 'instrument' and 'pair', or neither")
        return self


class PerpCursor(BaseModel, BaseConfig):
    """Pagination cursor: the sort date and id of the last row."""

    value: str = Field(..., description="Sort date in ISO format")
    id: UUID = Field(..., description="Row id")


class PerpCandleCursor(BaseModel, BaseConfig):
    """Pagination cursor for candles: the time of the last candle."""

    value: str = Field(..., description="Candle time in ISO format")


class PerpPaginatedResponse[T](BaseModel, BaseConfig):
    """Paginated response of the perp routes."""

    data: list[T] = Field(..., description="Array of items")
    next_cursor: PerpCursor | None = Field(
        default=None,
        description="Cursor for fetching the next page, null if no more pages",
    )


class _PerpPageParams(BaseModel, BaseConfig):
    from_: str | None = Field(
        default=None,
        serialization_alias="from",
        validation_alias="from",
        description="Start date as a string value in ISO format",
    )
    to: str | None = Field(
        default=None, description="End date as a string value in ISO format"
    )
    limit: int = Field(
        default=1000,
        ge=1,
        le=1000,
        description="Limit of items to return (max 1000, default 1000)",
    )
    cursor: PerpCursor | None = Field(
        default=None, description="`next_cursor` of the previous page"
    )


# Public data


class PerpTicker(PerpMarketKey):
    """Ticker of a perp market."""

    time: SkipValidation[str] = Field(..., description="ISO date string of the ticker")
    mark: SkipValidation[float] = Field(
        ..., description="Mark price (in USD). Values P&L, margin and funding"
    )
    last_price: SkipValidation[float] = Field(
        ..., description="Weighted last trade price of the reference exchanges"
    )
    prices: list[PriceBucket] = Field(
        ..., description="Price buckets for different order sizes"
    )
    funding_rate: SkipValidation[float] = Field(..., description="Current funding rate")
    funding_time: SkipValidation[str] = Field(
        ..., description="ISO date string of the next funding settlement"
    )
    quanto_adjustment_rate: SkipValidation[float] = Field(
        ...,
        description="Quanto adjustment rate for the next funding period (0 if none)",
    )
    exchanges_weights: SkipValidation[dict[str, float]] = Field(
        ..., description="Weight of each reference exchange"
    )
    price_change_24h: PriceChange24h | None = Field(
        default=None,
        alias="priceChange24h",
        description="Price change over the last 24 hours",
    )
    volume_24h: SkipValidation[float] | None = Field(
        default=None,
        alias="volume24h",
        description="24h trading volume in USD of the reference exchanges",
    )


class GetPerpCandlesParams(PerpMarketKey):
    from_: str | None = Field(
        default=None,
        serialization_alias="from",
        validation_alias="from",
        description="Start date as a string value in ISO format",
    )
    to: str | None = Field(
        default=None, description="End date as a string value in ISO format"
    )
    range: CandleResolution = Field(
        default="1m", description="Resolution of the OHLC candle"
    )
    limit: int = Field(
        default=1000,
        ge=1,
        le=1000,
        description="Number of entries to return (max 1000, default 1000)",
    )
    cursor: PerpCandleCursor | None = Field(
        default=None, description="`next_cursor` of the previous page"
    )


class PerpCandles(PerpMarketKey):
    """Candles of a perp market."""

    data: list[Candle]
    next_cursor: PerpCandleCursor | None = None


class PerpFundingSettlement(BaseModel, BaseConfig):
    """Funding settlement of a perp market."""

    id: SkipValidation[UUID] = Field(..., description="Funding settlement ID")
    time: SkipValidation[str] = Field(..., description="Funding settlement time")
    fixing_price: SkipValidation[float] = Field(..., description="Fixing price")
    funding_rate: SkipValidation[float] = Field(..., description="Funding rate")
    quanto_adjustment_rate: SkipValidation[float] = Field(
        ..., description="Quanto adjustment rate (0 if none)"
    )


class PerpFundingSettlements(PerpPaginatedResponse[PerpFundingSettlement]):
    """Funding settlements of a perp market."""

    instrument: PerpInstrument
    pair: str


class GetPerpFundingSettlementsParams(_PerpPageParams, PerpMarketKey): ...


# Isolated trades


class PerpStoploss(BaseModel, BaseConfig):
    mode: Literal["fixed", "trailing"] = Field(
        default="fixed",
        description="'fixed': `value` is a price. 'trailing': `value` is a distance as a fraction of price.",
    )
    value: float = Field(..., gt=0, description="Stop price or trailing distance")


class PerpOrder(PerpMarketKey):
    leverage: float = Field(..., description="Leverage of the position")
    side: Literal["buy", "sell"] = Field(
        ..., description="Trade side: buy (long) or sell (short)"
    )
    type: Literal["limit", "market"] = Field(
        ..., description="Trade type: limit (limit) or market (market)"
    )
    quantity: float | None = Field(
        default=None,
        gt=0,
        description="Quantity of the position, in the market's quantity unit",
    )
    margin: int | None = Field(
        default=None,
        gt=0,
        description="Margin of the position (in satoshis), to size the trade from it",
    )
    price: float | None = Field(
        default=None, gt=0, description="Price of the limit order"
    )
    stoploss: PerpStoploss | None = Field(default=None, description="Stop loss")
    takeprofit: float | None = Field(
        default=None, ge=0, description="Take profit price level"
    )
    client_id: str | None = Field(
        default=None,
        max_length=64,
        description="Optional custom data field (max 64 characters)",
    )

    @model_validator(mode="after")
    def validate_schema(self):
        if (self.quantity is None) == (self.margin is None):
            raise ValueError("Exactly one of quantity or margin must be set")
        if self.type == "limit" and self.price is None:
            raise ValueError("'price' is required when type='limit'")
        if self.type == "market" and self.price is not None:
            raise ValueError("'price' must not be set when type='market'")
        return self


class PerpTradeFields(BaseModel, BaseConfig):
    """Fields a perp trade adds to a futures trade."""

    instrument: SkipValidation[PerpInstrument]
    pair: SkipValidation[str]
    entry_notional_usd: SkipValidation[float] = Field(
        ..., description="Notional value at entry (in USD)"
    )
    exit_notional_usd: SkipValidation[float] | None = Field(
        default=None, description="Notional value at exit (in USD)"
    )
    entry_btc_price: SkipValidation[float] = Field(
        ..., description="BTC price at entry (in USD)"
    )
    sum_quanto_adjustment_fees: SkipValidation[float] = Field(
        default=0.0, description="Total quanto adjustment fees paid"
    )


class PerpOpenTrade(PerpTradeFields, FuturesOpenTrade): ...


class PerpRunningTrade(PerpTradeFields, FuturesRunningTrade): ...


class PerpRunningTradeRead(PerpRunningTrade):
    pl: SkipValidation[float] | None = Field(
        default=None, description="Unrealized P&L at the Mark price, null if unknown"
    )


class PerpClosedTrade(PerpTradeFields, FuturesClosedTrade):
    exit_notional_usd: SkipValidation[float] = 0.0


class PerpCanceledTrade(PerpTradeFields, FuturesCanceledTrade): ...


class PerpTradeParams(PerpMarketKey):
    id: UUID = Field(..., description="Trade ID")


class PerpAddMarginParams(PerpTradeParams):
    amount: int = Field(..., gt=0, description="Amount of margin to add (in satoshis)")


class PerpCashInParams(PerpTradeParams):
    amount: int = Field(..., gt=0, description="Amount to cash in (in satoshis)")


class PerpUpdateStoplossParams(PerpTradeParams):
    stoploss: PerpStoploss = Field(..., description="New stop loss")


class PerpUpdateTakeprofitParams(PerpTradeParams):
    value: float = Field(..., gt=0, description="New take profit price level")


class GetPerpTradesParams(_PerpPageParams, PerpMarketFilter): ...


class GetPerpFundingFeesParams(GetPerpTradesParams):
    trade_id: UUID | None = Field(default=None, description="Trade id to filter by")


class PerpFundingFee(BaseModel, BaseConfig):
    """Funding fee paid by an isolated perp trade."""

    instrument: SkipValidation[PerpInstrument]
    pair: SkipValidation[str]
    trade_id: SkipValidation[UUID] = Field(..., description="Trade ID")
    settlement_id: SkipValidation[UUID] = Field(
        ..., description="Funding settlement ID"
    )
    time: SkipValidation[str] = Field(..., description="Timestamp in ISO format")
    fee: SkipValidation[float] = Field(..., description="Funding fee amount")
    quanto_adjustment_fee: SkipValidation[float] = Field(
        default=0.0, description="Quanto adjustment fee amount"
    )
