import json
from lnmarkets import LNMClient
from typing import List, TypedDict
from lnmarkets.futures.types import FuturesClosedTrade


class CloseAllTradesResponse(TypedDict):
  trades: List[FuturesClosedTrade]


def close_all_trades(client: LNMClient) -> CloseAllTradesResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresclosealltrades
  """
  return json.loads(client.request_api('DELETE', '/futures/all/close', {}, True))

