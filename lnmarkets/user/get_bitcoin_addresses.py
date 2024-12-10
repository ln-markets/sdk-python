import json
from typing import TypedDict, NotRequired
from lnmarkets import LNMClient


class GetBitcoinAddressesParams(TypedDict):
  current: NotRequired[bool]


class BitcoinAddress(TypedDict):
  address: str
  creation_ts: int
  is_used: bool


def get_bitcoin_addresses(client: LNMClient, params: GetBitcoinAddressesParams = None) -> list[BitcoinAddress]:
  """
  @see https://docs.lnmarkets.com/api/operations/usergetbitcoinaddresses
  """
  return json.loads(client.request_api('GET', '/user/bitcoin/addresses', params, True)) 