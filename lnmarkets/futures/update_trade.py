import json
from lnmarkets import LNMClient
from lnmarkets.futures import UUID, FuturesOpenOrRunningTrade
from typing import TypedDict, Required, Literal


class UpdateTradeParams(TypedDict):
  id: Required[UUID]
  type: Required[Literal['stoploss', 'takeprofit']]
  value: Required[float]


def update_trade(client: LNMClient, params: UpdateTradeParams) -> FuturesOpenOrRunningTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresupdatetrade
  """
  return json.loads(client.request_api('PUT', '/futures', params, True))
