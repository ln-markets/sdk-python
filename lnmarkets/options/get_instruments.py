import json
from typing import List, TypedDict
from lnmarkets import LNMClient


class GetInstrumentsResponse(TypedDict):
  instruments: List[str]


def get_instruments(client: LNMClient) -> GetInstrumentsResponse:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgetinstruments
  """
  return json.loads(client.request_api('GET', '/options/instruments', {}, False)) 