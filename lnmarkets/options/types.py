from typing import TypedDict, Union, Literal
from lnmarkets import UUID

class OptionsInstrument(TypedDict):
  volatility: float

class OptionsMarketDetailsFees(TypedDict):
  trading: float

class OptionsMarketDetailsLimitsCount(TypedDict):
  max: float

class OptionsMarketDetailsLimitsMargin(TypedDict):
  max: float
  min: float

class OptionsMarketDetailsLimitsQuantity(TypedDict):
  max: float
  min: float

class OptionsMarketDetailsLimits(TypedDict):
  count: OptionsMarketDetailsLimitsCount
  margin: OptionsMarketDetailsLimitsMargin
  quantity: OptionsMarketDetailsLimitsQuantity

class OptionsMarketDetails(TypedDict):
  active: bool
  fees: OptionsMarketDetailsFees
  limits: OptionsMarketDetailsLimits

type OptionsSettlement = Literal['cash', 'physical']
type OptionsSide = Literal['b', 's']
type OptionsType = Literal['c', 'p']

class OptionsTrade(TypedDict):
  closed: bool
  closed_ts: float | None
  closing_fee: float
  creation_ts: float
  domestic: str
  exercised: bool
  expired: bool
  expiry_ts: float
  fixing_price: float | None
  forward: float
  forward_point: float
  id: UUID
  leg_id: UUID
  maintenance_margin: float
  margin: float
  opening_fee: float
  physical_delivery_id: str | None
  pl: float
  quantity: float
  running: bool
  settlement: OptionsSettlement
  side: OptionsSide
  strike: float
  type: OptionsType
  uid: UUID
  volatility: float

class OptionsTradeClosedCash(OptionsTrade, TypedDict):
  closed: Literal[True]
  closed_ts: float
  expired: Literal[False]
  fixing_price: float
  physical_delivery_id: None

class OptionsTradeClosedPhysical(OptionsTrade, TypedDict):
  closed: Literal[True]
  closed_ts: float
  fixing_price: float
  physical_delivery_id: str

OptionsTradeClosed = Union[OptionsTradeClosedCash, OptionsTradeClosedPhysical]

class OptionsTradeExpiredCash(OptionsTrade, TypedDict):
  closed: Literal[False]
  closed_ts: float
  expired: Literal[True]
  fixing_price: float
  physical_delivery_id: None

class OptionsTradeExpiredPhysical(OptionsTrade, TypedDict):
  closed: Literal[False]
  closed_ts: float
  expired: Literal[True]
  fixing_price: float

class OptionsTradeExpiredPhysicalDelivered(OptionsTradeExpiredPhysical, TypedDict):
  physical_delivery_id: str

class OptionsTradeExpiredPhysicalNotDelivered(OptionsTradeExpiredPhysical, TypedDict):
  physical_delivery_id: None

OptionsTradeExpired = Union[
  OptionsTradeExpiredCash,
  OptionsTradeExpiredPhysicalDelivered,
  OptionsTradeExpiredPhysicalNotDelivered
]

class OptionsTradeOrder(TypedDict):
  instrument_name: str
  quantity: float
  settlement: OptionsSettlement
  side: OptionsSide

class OptionsTradeRunning(OptionsTrade, TypedDict):
  closed: Literal[False]
  closed_ts: None
  physical_delivery_id: None

class OptionsTradeRunningWithDelta(OptionsTradeRunning, TypedDict):
  delta: float

type OptionsTradeStatus = Literal['closed', 'running']

class OptionsTradeWithDelta(OptionsTrade, TypedDict):
  delta: float | None

class OptionsVolatilityIndex(TypedDict):
  volatility_index: float
