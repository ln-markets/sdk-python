import json
from lnmarkets.futures.types import UUID
from lnmarkets import LNMClient
from typing import List, TypedDict, Optional, NotRequired


class FixingHistoryParams(TypedDict):
  from_ts: NotRequired[int]
  to: NotRequired[int]
  limit: NotRequired[int]


class FixingHistory(TypedDict):
  fee: float
  fixing_id: UUID
  id: UUID
  ts: int


class FixingHistoryResponse(TypedDict):
  fixingHistory: List[FixingHistory]


def get_fixing_history(client: LNMClient, params: Optional[FixingHistoryParams] = None) -> FixingHistoryResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetfixinghistory
  """
  return json.loads(client.request_api('GET', '/futures/history/fixing', params or {}, False))
