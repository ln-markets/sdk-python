from typing import List, Literal, Optional, TypedDict, Union
from lnmarkets import UUID


class FuturesCanceledTrade(TypedDict):
  canceled: Literal[True]
  closed: Literal[False]
  closed_ts: int
  market_filled_ts: None
  open: Literal[False]
  running: Literal[False]
  type: Literal['l']


class FuturesClosedTrade(TypedDict):
  canceled: Literal[False]
  closed: Literal[True]
  closed_ts: int
  exit_price: float
  market_filled_ts: int
  open: Literal[False]
  running: Literal[False]


class FuturesMarketDetailsTier(TypedDict):
  fees: float
  min_volume: float


class FuturesMarketDetailsCarry(TypedDict):
  hours: List[int]
  min: float


class FuturesMarketDetailsTrading(TypedDict):
  tiers: List[FuturesMarketDetailsTier]


class FuturesMarketDetailsFees(TypedDict):
  carry: FuturesMarketDetailsCarry
  trading: FuturesMarketDetailsTrading


class FuturesMarketDetailsCount(TypedDict):
  max: int


class FuturesMarketDetailsLeverage(TypedDict):
  max: float
  min: float


class FuturesMarketDetailsQuantity(TypedDict):
  max: float
  min: float
  trade: float


class FuturesMarketDetailsLimits(TypedDict):
  count: FuturesMarketDetailsCount
  leverage: FuturesMarketDetailsLeverage
  quantity: FuturesMarketDetailsQuantity


class FuturesMarketDetails(TypedDict):
  active: bool
  fees: FuturesMarketDetailsFees
  limits: FuturesMarketDetailsLimits


class FuturesOpenTrade(TypedDict):
  canceled: Literal[False]
  closed: Literal[False]
  closed_ts: None
  market_filled_ts: None
  running: Literal[False]
  type: Literal['l']


class FuturesRunningTrade(TypedDict):
  canceled: Literal[False]
  closed: Literal[False]
  closed_ts: None
  market_filled_ts: int
  running: Literal[True]


type FuturesOpenOrRunningTrade = Union[FuturesOpenTrade, FuturesRunningTrade]


class FuturesTicker(TypedDict):
  ask_price: float
  bid_price: float
  carry_fee_rate: float
  carry_fee_timestamp: int
  index: float
  last_price: float


class FuturesTrade(TypedDict):
  canceled: bool
  closed: bool
  closed_ts: Optional[int]
  closing_fee: float
  creation_ts: int
  entry_margin: Optional[float]
  entry_price: Optional[float]
  exit_price: Optional[float]
  id: UUID
  last_update_ts: int
  leverage: float
  liquidation: float
  maintenance_margin: float
  margin: float
  market_filled_ts: Optional[int]
  open: bool
  opening_fee: float
  pl: float
  price: float
  quantity: float
  running: bool
  side: Literal['b', 's']
  sum_carry_fees: float
  type: Literal['l', 'm']
  uid: UUID


type FuturesTradeSide = Literal['b', 's']
type FuturesTradeStatus = Literal['closed', 'open', 'running']
type FuturesTradeType = Literal['l', 'm']


class OHLC(TypedDict):
  close: float
  high: float
  low: float
  open: float
  time: int
  volume: float


type OHLCRange = Literal[
  '1',
  '1D',
  '1M',
  '1W',
  '3',
  '3M',
  '5',
  '15',
  '30',
  '60',
  '120',
  '240'
]
