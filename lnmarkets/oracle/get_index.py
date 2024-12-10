import json
from typing import TypedDict, Required, NotRequired, List
from lnmarkets import LNMClient


class GetIndexParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  limit: NotRequired[int]


class IndexEntry(TypedDict):
  index: float
  time: int


def get_index(client: LNMClient, params: GetIndexParams) -> List[IndexEntry]:
  """
  @see https://docs.lnmarkets.com/api/operations/oraclegetindex
  """
  return json.loads(client.request_api('GET', '/oracle', params, False)) 