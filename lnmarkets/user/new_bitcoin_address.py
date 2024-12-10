import json
from typing import TypedDict, Required
from lnmarkets import LNMClient


class NewBitcoinAddressParams(TypedDict):
  format: Required[str]  # Literal['p2tr', 'p2wpkh']


class NewBitcoinAddressResponse(TypedDict):
  address: str
  creation_ts: int


def new_bitcoin_address(client: LNMClient, params: NewBitcoinAddressParams) -> NewBitcoinAddressResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/usernewbitcoinaddress
  """
  return json.loads(client.request_api('POST', '/user/bitcoin/address', params, True)) 