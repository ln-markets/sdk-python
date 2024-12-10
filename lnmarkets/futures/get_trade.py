import json
from lnmarkets.futures.types import FuturesTrade
from lnmarkets import LNMClient
from typing import Required, UUID, TypedDict


class GetTradeParams(TypedDict):
  id: Required[UUID]


def get_trade(client: LNMClient, params: GetTradeParams) -> FuturesTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgettrade
  """
  return json.loads(client.request_api('GET', f'/futures/trades/{params["id"]}', {}, False))
