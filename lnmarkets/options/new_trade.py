import json
from typing import TypedDict, Required
from lnmarkets.options.types import OptionsSettlement, OptionsSide, OptionsTradeRunning
from lnmarkets import LNMClient


class NewTradeParams(TypedDict):
  instrument_name: Required[str]
  quantity: Required[int]
  settlement: Required[OptionsSettlement]
  side: Required[OptionsSide]


def new_trade(client: LNMClient, params: NewTradeParams) -> OptionsTradeRunning:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsnewtrade
  """
  return json.loads(client.request_api('POST', '/options', params, True)) 