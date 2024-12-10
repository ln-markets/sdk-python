import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.swaps.types import Swap, SwapAsset


class NewSwapParams(TypedDict):
  in_amount: Required[int]
  in_asset: Required[SwapAsset]
  out_asset: Required[SwapAsset]


def new_swap(client: LNMClient, params: NewSwapParams) -> Swap:
  """
  @see https://docs.lnmarkets.com/api/operations/swapsnewswap
  """
  return json.loads(client.request_api('POST', '/swap', params, True)) 