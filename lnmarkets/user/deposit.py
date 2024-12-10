import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID


class DepositParams(TypedDict):
  amount: Required[float]


class DepositResponse(TypedDict):
  deposit_id: UUID
  expiry: int
  payment_request: str


def deposit(client: LNMClient, params: DepositParams) -> DepositResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/userdeposit
  """
  return json.loads(client.request_api('POST', '/user/deposit', params, True)) 