import json
from lnmarkets import LNMClient, UUID
from typing import TypedDict, Required
from lnmarkets.futures.types import FuturesClosedTrade


class CloseTradeParams(TypedDict):
  id: Required[UUID]


def close_trade(client: LNMClient, params: CloseTradeParams) -> FuturesClosedTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresclosetrade
  """
  return json.loads(client.request_api('DELETE', '/futures', params, True))
