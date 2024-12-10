import json
from lnmarkets import LNMClient, UUID
from typing import TypedDict, Required
from lnmarkets.futures.types import FuturesRunningTrade


class CashInParams(TypedDict):
  amount: Required[float]
  id: Required[UUID]


def cash_in(client: LNMClient, params: CashInParams) -> FuturesRunningTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futurescashin
  """
  return json.loads(client.request_api('POST', '/futures/cash-in', params, True))
