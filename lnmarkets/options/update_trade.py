import json
from typing import TypedDict, Required
from lnmarkets.options.types import UUID, OptionsSettlement, OptionsTradeRunningWithDelta
from lnmarkets import LNMClient


class UpdateTradeParams(TypedDict):
  id: Required[UUID]
  settlement: Required[OptionsSettlement]


def update_trade(client: LNMClient, params: UpdateTradeParams) -> OptionsTradeRunningWithDelta:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsupdatetrade
  """
  return json.loads(client.request_api('PUT', '/options', params, True)) 