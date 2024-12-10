import json
from lnmarkets import LNMClient, UUID
from typing import TypedDict, Required
from lnmarkets.futures.types import FuturesCanceledTrade


class CancelTradeParams(TypedDict):
  id: Required[UUID]


def cancel_trade(client: LNMClient, params: CancelTradeParams) -> FuturesCanceledTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futurescanceltrade
  """
  return json.loads(client.request_api('POST', '/futures/cancel', params, True))