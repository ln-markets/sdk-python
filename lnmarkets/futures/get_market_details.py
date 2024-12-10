import json
from lnmarkets import LNMClient
from lnmarkets.futures.types import FuturesMarketDetails


def get_market_details(client: LNMClient) -> FuturesMarketDetails:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetfuturesmarket
  """
  return json.loads(client.request_api('GET', '/futures/market', {}, False))