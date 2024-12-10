import json
from lnmarkets import LNMClient
from typing import TypedDict, Required, NotRequired
from lnmarkets.futures import (
  FuturesOpenOrRunningTrade,
  FuturesTradeSide,
  FuturesTradeType,
)


class NewTradeParams(TypedDict):
  leverage: Required[float]
  side: Required[FuturesTradeSide]
  type: Required[FuturesTradeType]
  margin: NotRequired[float]
  price: NotRequired[float]
  quantity: NotRequired[float]
  stoploss: NotRequired[float]
  takeprofit: NotRequired[float]


def new_trade(client: LNMClient, params: NewTradeParams) -> FuturesOpenOrRunningTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresnewtrade
  """
  return json.loads(client.request_api('POST', '/futures', params, True))
