import json
from typing import TypedDict, Required
from lnmarkets import LNMClient


class TransferParams(TypedDict):
  amount: Required[float]
  to_username: Required[str]


class TransferResponse(TypedDict):
  amount: float
  to: str


def transfer(client: LNMClient, params: TransferParams) -> TransferResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/usertransfer
  """
  return json.loads(client.request_api('POST', '/user/transfer', params, True)) 