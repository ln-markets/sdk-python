import json
from lnmarkets.user.types import Leaderboard
from lnmarkets import LNMClient


def get_leaderboard(client: LNMClient) -> Leaderboard:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetleaderboard
  """
  return json.loads(client.request_api('GET', '/futures/leaderboard', {}, False))
