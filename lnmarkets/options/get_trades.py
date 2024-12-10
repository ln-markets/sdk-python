import json
from typing import List, TypedDict, Required, NotRequired
from lnmarkets.options.types import OptionsTrade, OptionsTradeStatus
from lnmarkets import LNMClient


class GetTradesParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  status: Required[OptionsTradeStatus]
  limit: NotRequired[int]


def get_trades(client: LNMClient, params: GetTradesParams) -> List[OptionsTrade]:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgettrades
  """
  return json.loads(client.request_api('GET', '/options/trades', params, True)) 