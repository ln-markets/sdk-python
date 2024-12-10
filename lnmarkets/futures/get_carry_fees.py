import json
from lnmarkets.futures.types import UUID
from lnmarkets import LNMClient
from typing import List, TypedDict, Required, NotRequired


class CarryFeesHistoryParams(TypedDict):
  from_ts: Required[int]
  to: Required[int]
  limit: NotRequired[int]


class CarryFee(TypedDict):
  fee: float
  fixing_id: UUID
  id: UUID
  ts: int


class CarryFeesHistoryResponse(TypedDict):
  carryFees: List[CarryFee]


def get_carry_fees_history(client: LNMClient, params: CarryFeesHistoryParams) -> CarryFeesHistoryResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/futuresgetcarryfees
  """
  return json.loads(client.request_api('GET', '/futures/carry-fees', params, False))
