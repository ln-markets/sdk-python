import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID, Currency


class WithdrawSyntheticUsdParams(TypedDict):
  amount: Required[float]
  currency: Required[Currency]


class WithdrawSyntheticUsdResponse(TypedDict):
  amount: float
  currency: Currency
  fee_reserve: float
  min_balance_after: float
  quote_id: UUID
  valid_until: int


def withdraw_synthetic_usd(client: LNMClient, params: WithdrawSyntheticUsdParams) -> WithdrawSyntheticUsdResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/userwithdrawalsyntheticusd
  """
  return json.loads(client.request_api('POST', '/user/withdraw/susd', params, True)) 