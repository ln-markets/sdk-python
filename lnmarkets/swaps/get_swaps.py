import json
from typing import TypedDict, NotRequired
from lnmarkets import LNMClient
from lnmarkets.swaps.types import Swap


class GetSwapsParams(TypedDict):
  from_ts: NotRequired[int]
  to: NotRequired[int]
  limit: NotRequired[int]


def get_swaps(client: LNMClient, params: GetSwapsParams = None) -> list[Swap]:
  """
  @see https://docs.lnmarkets.com/api/operations/swapsgetswaps
  """
  return json.loads(client.request_api('GET', '/swap', params, True)) 