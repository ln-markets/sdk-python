import json
from typing import List, TypedDict, Required, NotRequired
from lnmarkets import LNMClient
from lnmarkets.futures.types import FuturesTrade, FuturesTradeStatus


class GetTradesParams(TypedDict):
  type: Required[FuturesTradeStatus]
  from_ts: NotRequired[int]
  to: NotRequired[int]
  limit: NotRequired[int]


def get_trades(client: LNMClient, params: GetTradesParams) -> List[FuturesTrade]:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgettrades
  """
  return json.loads(client.request_api('GET', '/futures', params, True))
