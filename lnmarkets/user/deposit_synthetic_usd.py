import json
from typing import TypedDict, Required
from lnmarkets import LNMClient
from lnmarkets.user.types import UUID, Currency


class DepositSyntheticUsdParams(TypedDict):
  amount: Required[float]
  currency: Required[Currency]


class DepositSyntheticUsdResponse(TypedDict):
  deposit_id: UUID
  expiry: int
  payment_request: str
  synthetic_usd_amount: float


def deposit_synthetic_usd(client: LNMClient, params: DepositSyntheticUsdParams) -> DepositSyntheticUsdResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/userdepositsyntheticusd
  """
  return json.loads(client.request_api('POST', '/user/deposit/susd', params, True)) 