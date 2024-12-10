import json
from lnmarkets.options.types import OptionsMarketDetails
from lnmarkets import LNMClient


def get_market_details(client: LNMClient) -> OptionsMarketDetails:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgetoptionsmarket
  """
  return json.loads(client.request_api('GET', '/options', {}, False)) 