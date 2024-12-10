import json
from typing import TypedDict, Required
from lnmarkets.options.types import UUID, OptionsTrade
from lnmarkets import LNMClient


class GetTradeParams(TypedDict):
  id: Required[UUID]


def get_trade(client: LNMClient, params: GetTradeParams) -> OptionsTrade:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgettrade
  """
  return json.loads(client.request_api('GET', f'/options/trades/{params["id"]}', {}, True)) 