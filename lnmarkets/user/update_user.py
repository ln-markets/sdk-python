import json
from typing import TypedDict, NotRequired
from lnmarkets import LNMClient
from lnmarkets.user.types import User


class UpdateUserParams(TypedDict):
  auto_withdraw_enabled: NotRequired[bool]
  auto_withdraw_lightning_address: NotRequired[bool]
  nostr_pubkey: NotRequired[str]
  show_leaderboard: NotRequired[bool]
  username: NotRequired[str]
  use_taproot_addresses: NotRequired[bool]


def update_user(client: LNMClient, params: UpdateUserParams) -> User:
  """
  @see https://docs.lnmarkets.com/api/operations/userupdate
  """
  return json.loads(client.request_api('PUT', '/user', params, True)) 