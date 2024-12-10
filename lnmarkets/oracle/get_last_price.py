import json
from typing import TypedDict, Required, NotRequired
from lnmarkets import LNMClient


class GetLastPriceParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  limit: NotRequired[int]


class LastPriceResponse(TypedDict):
  last_price: float
  time: int


def get_last_price(client: LNMClient, params: GetLastPriceParams) -> LastPriceResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/oraclegetlastprice
  """
  return json.loads(client.request_api('GET', '/oracle/last-price', params, False)) 