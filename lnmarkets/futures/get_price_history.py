import json
from typing import List, TypedDict, Required, NotRequired
from lnmarkets import LNMClient


class HistoryParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  limit: NotRequired[int]


def get_price_history(client: LNMClient, params: HistoryParams) -> List[dict]:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetpricehistory
  """
  return json.loads(client.request_api('GET', '/futures/history/price', params, False))

