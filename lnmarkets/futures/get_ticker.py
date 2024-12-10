import json
from lnmarkets import LNMClient
from lnmarkets.futures.types import FuturesTicker


def get_ticker(client: LNMClient) -> FuturesTicker:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetticker
  """
  return json.loads(client.request_api('GET', '/futures/ticker', {}, False))

