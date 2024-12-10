import json
from lnmarkets import LNMClient
from typing import List, TypedDict, Optional, NotRequired


class HistoryParams(TypedDict):
  from_ts: NotRequired[int]
  to: NotRequired[int]
  limit: NotRequired[int]


class IndexHistory(TypedDict):
  time: int
  value: float


class IndexHistoryResponse(TypedDict):
  indexHistory: List[IndexHistory]


def get_index_history(client: LNMClient, params: Optional[HistoryParams] = None) -> IndexHistoryResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetindexhistory
  """
  return json.loads(client.request_api('GET', '/futures/history/index', params or {}, False))
