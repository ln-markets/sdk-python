import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.swaps.types import UUID, Swap


class GetSwapParams(TypedDict):
  swap_id: Required[UUID]


def get_swap(client: LNMClient, params: GetSwapParams) -> Swap:
  """
  @see https://docs.lnmarkets.com/api/operations/swapsgetswap
  """
  return json.loads(client.request_api('GET', f'/swap/{params["swap_id"]}', {}, True)) 