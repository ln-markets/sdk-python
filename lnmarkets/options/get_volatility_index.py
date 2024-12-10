import json
from lnmarkets.options.types import OptionsVolatilityIndex
from lnmarkets import LNMClient


def get_volatility_index(client: LNMClient) -> OptionsVolatilityIndex:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgetvolatilityindex
  """
  return json.loads(client.request_api('GET', '/options/volatility-index', {}, False)) 