import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID, Deposit


class GetDepositParams(TypedDict):
  deposit_id: Required[UUID]


def get_deposit(client: LNMClient, params: GetDepositParams) -> Deposit:
  """
  @see https://docs.lnmarkets.com/api/operations/usergetdeposit
  """
  return json.loads(client.request_api('GET', f'/user/deposit/{params["deposit_id"]}', {}, True)) 