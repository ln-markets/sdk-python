from typing import TypedDict, List, Optional, Union, Literal, Any
from lnmarkets import UUID

class ApiKeyCreation(TypedDict):
  name: str
  passphrase: str
  permissions: List[str]

class BitcoinDeposit(TypedDict):
  amount: float
  block_id: Optional[str]
  confirmation_height: Optional[int]
  confirmed_ts: Optional[int]
  id: str
  is_confirmed: bool
  transaction_id: str
  ts: int

type Currency = Literal['btc', 'usd']

type Deposit = Union['BitcoinDeposit', 'InternalTransfer', 'LightningDeposit']

type DepositType = Literal['bitcoin', 'internal', 'lightning']

type FeeTier = Literal[0, 1, 2, 3]

class FetchTransactionsRequest(TypedDict, total=False):
  cursor: int
  from_: int
  limit: int
  to: int
  types: str

type GenericDeposit = Union['GenericDepositError', 'GenericDepositSuccess']

class GenericDepositBase(TypedDict):
  amount: float
  comment: Optional[str]
  id: str
  success: bool
  transaction_id_or_hash: str
  ts: int
  type: 'DepositType'

class GenericDepositError(TypedDict):
  amount: float
  comment: Optional[str]
  id: str
  success: Literal[False]
  transaction_id_or_hash: Optional[str]
  ts: int
  type: 'DepositType'

class GenericDepositSuccess(GenericDepositBase):
  success: Literal[True]

class GenericOnChainWithdrawal(TypedDict):
  amount: float
  fee: float
  id: str
  ts: int
  status: 'OnChainWithdrawalStatus'
  transaction_id_or_hash: Optional[str]
  type: Literal['bitcoin']

type GenericWithdrawal = Union['GenericWithdrawalError', 'GenericWithdrawalSuccess']

class GenericWithdrawalBase(TypedDict):
  amount: float
  fee: float
  id: str
  success: bool
  transaction_id_or_hash: str
  ts: int
  type: Literal['internal', 'lightning']

class GenericWithdrawalError(TypedDict):
  amount: float
  id: str
  success: Literal[False]
  transaction_id_or_hash: str
  ts: int
  type: Literal['internal', 'lightning']
  fee: Optional[float]

class GenericWithdrawalSuccess(GenericWithdrawalBase):
  success: Literal[True]

class InternalTransfer(TypedDict):
  amount: float
  from_username: str
  id: str
  success: bool
  to_username: str
  ts: int

class InternalWithdrawalCondensed(TypedDict):
  amount: float
  id: str
  success: bool
  to_username: str
  ts: int
  type: Literal['internal']

class LeaderboardEntry(TypedDict):
  direction: int
  pl: float
  username: str

class Leaderboard(TypedDict):
  all_time: List[LeaderboardEntry]
  daily: List[LeaderboardEntry]
  monthly: List[LeaderboardEntry]
  weekly: List[LeaderboardEntry]

class LightningDeposit(TypedDict):
  amount: float
  comment: Optional[str]
  id: str
  payment_hash: str
  success: bool
  success_ts: Optional[int]
  ts: int

class LightningWithdrawalCondensed(TypedDict):
  amount: float
  destination: Optional[str]
  fee: float
  id: str
  payment_hash: str
  success: bool
  ts: int
  type: Literal['lightning']

class NewApiKey(TypedDict):
  creation_ts: int
  id: str
  key: str
  last_modified: int
  name: Optional[str]
  permissions: List[str]
  secret: str

class OnChainWithdrawalCondensed(TypedDict):
  address: str
  amount: float
  fee: float
  id: str
  status: 'OnChainWithdrawalStatus'
  transaction_id: str
  ts: int
  type: Literal['bitcoin']

type OnChainWithdrawalStatus = Literal['confirmed', 'failed', 'pending']

class TotpSetup(TypedDict):
  backup_codes: List[str]
  secret: str
  url: str

class User(TypedDict):
  account_type: str
  auto_withdraw_enabled: bool
  auto_withdraw_lightning_address: Optional[str]
  balance: float
  email: Optional[str]
  email_confirmed: bool
  fee_tier: FeeTier
  linking_public_key: Optional[str]
  metrics: Any
  nostr_pubkey: Optional[str]
  role: str
  show_leaderboard: bool
  synthetic_usd_balance: float
  totp_enabled: bool
  uid: UUID
  username: str
  use_taproot_addresses: bool
  webauthn_enabled: bool

type WithdrawalCondensed = Union[InternalWithdrawalCondensed, LightningWithdrawalCondensed, OnChainWithdrawalCondensed]
