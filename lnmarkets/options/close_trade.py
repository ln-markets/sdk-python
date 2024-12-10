import json
from typing import TypedDict, Required
from lnmarkets.options.types import UUID, OptionsTradeClosed
from lnmarkets import LNMClient


class CloseTradeParams(TypedDict):
  id: Required[UUID]


def close_trade(client: LNMClient, params: CloseTradeParams) -> OptionsTradeClosed:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsclosetrade
  """
  return json.loads(client.request_api('DELETE', '/options', params, True)) 