import json
from lnmarkets import LNMClient
from lnmarkets.user.types import User


def get_user(client: LNMClient) -> User:
  """
  @see https://docs.lnmarkets.com/api/operations/usergetuser
  """
  return json.loads(client.request_api('GET', '/user', {}, True))
