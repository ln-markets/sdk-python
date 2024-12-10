import json
from typing import NotRequired, Required, TypedDict
from lnmarkets import LNMClient
from lnmarkets.futures.types import FuturesRunningTrade, UUID


class AddMarginParams(TypedDict):
  amount: Required[float]
  id: NotRequired[UUID]


def add_margin(client: LNMClient, params: AddMarginParams) -> FuturesRunningTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresaddmargin
  """
  return json.loads(client.request_api('POST', '/futures/margin', params, True))
