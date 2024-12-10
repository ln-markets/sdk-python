import json
from typing import TypedDict, Required, NotRequired
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID


class WithdrawParams(TypedDict):
  invoice: Required[str]
  quote_id: NotRequired[UUID]


class WithdrawResponse(TypedDict):
  amount: NotRequired[float]
  fee: NotRequired[float]
  id: UUID
  payment_hash: NotRequired[str]
  success_time: NotRequired[int]


def withdraw(client: LNMClient, params: WithdrawParams) -> WithdrawResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/userwithdraw
  """
  return json.loads(client.request_api('POST', '/user/withdraw', params, True)) 