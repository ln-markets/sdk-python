import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID, WithdrawalCondensed


class GetWithdrawalParams(TypedDict):
  id: Required[UUID]


def get_withdrawal(client: LNMClient, params: GetWithdrawalParams) -> WithdrawalCondensed:
  """
  @see https://docs.lnmarkets.com/api/operations/usergetwithdrawal
  """
  return json.loads(client.request_api('GET', f'/user/withdrawals/{params["id"]}', {}, True)) 