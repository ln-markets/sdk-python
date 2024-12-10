import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.swaps.types import UUID, Swap, SwapSource


class GetSwapBySourceIdParams(TypedDict):
  source_id: Required[UUID]
  source: Required[SwapSource]


def get_swap_by_source_id(client: LNMClient, params: GetSwapBySourceIdParams) -> Swap:
  """
  @see https://docs.lnmarkets.com/api/operations/swapsgetswapbysourceid
  """
  return json.loads(client.request_api('GET', f'/swap/source/{params["source_id"]}', {'source': params['source']}, True)) 