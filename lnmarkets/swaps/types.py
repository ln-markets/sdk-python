from typing import TypedDict, NotRequired, Literal
from lnmarkets.swaps.types import UUID

type SwapAsset = Literal['BTC', 'USD']

type SwapSource = Literal[
  'deposit',
  'fee-refund',
  'swap', 
  'withdrawal',
  'withdrawal-failed'
]

class Swap(TypedDict):
  creation_ts: int
  id: UUID
  in_amount: int
  in_asset: SwapAsset
  out_amount: int
  out_asset: SwapAsset
  source: NotRequired[SwapSource]
  source_id: NotRequired[UUID]
  uid: UUID


