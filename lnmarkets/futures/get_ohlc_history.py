import json
from lnmarkets.futures.types import OHLC, OHLCRange
from typing import List, TypedDict, Required, NotRequired
from lnmarkets import LNMClient


class OHLCHistoryParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  range: Required[OHLCRange]
  limit: NotRequired[int]


def get_ohlc_history(client: LNMClient, params: OHLCHistoryParams) -> List[OHLC]:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetohlcs
  """
  return json.loads(client.request_api('GET', '/futures/ohlcs', params, False))
