import json
from typing import List
from lnmarkets.options.types import OptionsTradeClosed
from lnmarkets import LNMClient


def close_all_trades(client: LNMClient) -> List[OptionsTradeClosed]:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsclosealltrades
  """
  return json.loads(client.request_api('DELETE', '/options/all/close', {}, True)) 