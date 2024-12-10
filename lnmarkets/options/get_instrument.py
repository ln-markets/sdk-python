import json
from typing import TypedDict, Required
from lnmarkets.options.types import OptionsInstrument
from lnmarkets import LNMClient


class GetInstrumentParams(TypedDict):
  instrument_name: Required[str]


def get_instrument(client: LNMClient, params: GetInstrumentParams) -> OptionsInstrument:
  """
  @see https://docs.lnmarkets.com/api/operations/optionsgetinstrument
  """
  return json.loads(client.request_api('GET', '/options/instrument', params, False)) 