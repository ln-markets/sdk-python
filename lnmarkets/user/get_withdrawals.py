import json
from lnmarkets import LNMClient
from lnmarkets.user.types import WithdrawalCondensed


def get_withdrawals(client: LNMClient) -> list[WithdrawalCondensed]:
  """
  @see https://docs.lnmarkets.com/api/operations/usergetwithdrawals
  """
  return json.loads(client.request_api('GET', '/user/withdraw', {}, True)) 