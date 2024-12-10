import json
from lnmarkets import LNMClient
from typing import List, TypedDict
from lnmarkets.futures.types import FuturesCanceledTrade


class CancelAllTradesResponse(TypedDict):
  trades: List[FuturesCanceledTrade]


def cancel_all_trades(client: LNMClient) -> CancelAllTradesResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/futurescancelalltrades
  """
  return json.loads(client.request_api('DELETE', '/futures/all/cancel', {}, True))
