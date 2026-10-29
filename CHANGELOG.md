# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-10-29

Multi-market perp API (`/v3/perp`) and `GET /v3/markets`.

### Added

- `client.get_markets()` (`GET /v3/markets`): the released markets, plus the early-access markets your API key can access. Returns `Market` models (`lnmarkets_sdk.rest.v3.models.markets`).
- `client.perp` (`PerpClient`) for `/v3/perp`: `get_ticker()`, `get_candles()` and `get_funding_settlements()`.
- `client.perp.isolated` (`PerpIsolatedClient`) for `/v3/perp/isolated`: `new_trade()`, `cancel()`, `cancel_all()`, `close()`, `add_margin()`, `cash_in()`, `update_stoploss()`, `update_takeprofit()`, `remove_stoploss()`, `remove_takeprofit()`, `get_open_trades()`, `get_running_trades()`, `get_closed_trades()`, `get_canceled_trades()` and `get_funding_fees()`.
- Perp models in `lnmarkets_sdk.rest.v3.models.perp`. Every perp call takes the market key (`instrument` + `pair`). Trades, tickers, funding settlements and funding fees include the quanto fields (`quanto_adjustment_rate`, `quanto_adjustment_fee`, `sum_quanto_adjustment_fees`), the notional fields, and the `mark` price.
- Cursor pagination for the perp history reads: pass `next_cursor` back as `cursor`. The cursor is an object (`PerpCursor(value=..., id=...)`), sent as `cursor[value]` and `cursor[id]` in the query.
- The public perp routes and `get_markets()` sign the request when the client has credentials, so early-access markets work.

### Deprecated

- `client.futures.get_ticker()`, `get_candles()`, `get_funding_settlements()` and every `client.futures.isolated` method. They still work and raise a `DeprecationWarning` that names the `client.perp` method to use with `instrument="inverse_perp", pair="btc_usd"`. `client.futures.get_leaderboard()` and `client.futures.cross` have no perp replacement yet and are not deprecated.

### Fixed

- Request signature for bodies with nested whole floats (e.g. `{"stoploss": {"value": 64000.0}}`): nested values are now sent as `64000`, like the server's `JSON.stringify`, so the signature matches.
- `futures.isolated.update_takeprofit()` no longer prints its params.

## [0.2.0] - 2026-10-26

Models re-synced with the published v3 API reference.

### Added

- `Ticker.time`, `Ticker.price_change_24h` (`ratio`, `updated_at`) and `Ticker.exchanges_weights`.
- `FuturesOrder.stoploss_mode` (`"fixed"` | `"trailing"`), so a trailing stop can be set when opening an isolated trade. `stoploss` no longer has to be a multiple of `0.5`, since a trailing distance is a fraction of the price.
- `GetNotificationsParams.read` filter (the API returns unread notifications by default).
- `under_review`, `not_credited` and `on_hold` on-chain deposit statuses, both as a `get_on_chain_deposits()` filter and on `OnChainDeposit.status`.
- `CreateSwapOutput.id`.

### Fixed

- `account.withdraw_on_chain()` failed validation on success: `WithdrawOnChainResponse` required `uid`, `updated_at`, `block_id`, `confirmation_height` and `fee`, which the API does not return. Those fields are removed.
- `futures.cross.new_order()` required `client_id`; it is optional (max 64 characters), as in the API.
- `GetCandlesParams.from_` is optional, as in the API.

### Removed

- **Breaking:** `client.oracle` (`OracleClient`) and the `lnmarkets_sdk.rest.v3.models.oracle` module (`OracleIndex`, `OracleLastPrice`, `GetIndexParams`, `GetLastPriceParams`). LN Markets removed `GET /oracle/index` and `GET /oracle/last-price` from the API on 2026-07-17, so these methods only returned `404`. Use `client.futures.get_ticker()` (`index` and `last_price` fields) for current values and `client.futures.get_candles()` for price history.

## [0.1.4] - 2026-07-16

### Added

- Automatic retry with exponential backoff for transient failures. `LNMClient` now retries `503`/`502`/`504`/`429` responses and connection-phase transport errors (`ConnectError`, `ConnectTimeout`, `PoolTimeout`), honoring a `Retry-After` header on `429`. Read/write timeouts are deliberately not retried, so non-idempotent trades cannot be double-submitted. The auth signature is regenerated on every attempt so its timestamp stays fresh across backoff delays.
- Retry configuration on `APIClientConfig`: `max_retries` (default `3`), `retry_base_delay` (default `1.0`s), `retry_max_delay` (default `8.0`s). Set `max_retries=0` to disable retrying. The base delay defaults to the rate-limit window so retries never trigger a `429`.
- `tenacity` dependency (backoff engine).

### Changed

- Migrated the test/dev network from `testnet4` to `signet`. The `APINetwork` type is now `"mainnet" | "signet"` (was `"testnet4"`) and the resolved host is `api.signet.lnmarkets.com`. Pass `network="signet"` instead of `network="testnet4"`.
- Integration tests now guarantee cleanup and guard against low funds: a session teardown cancels resting orders/trades, closes running trades and the cross position, and returns cross margin to the balance (best-effort, never fails the suite); a balance-floor guard skips trading tests when signet funds run low instead of failing with opaque insufficient-margin errors.

## [0.1.3] - 2026-07-03

No user-facing library changes; identical behavior to 0.1.2 (release and CI tooling only).

## [0.1.2] - 2026-07-02

### Added

- `futures.isolated.remove_stoploss()` method — maps to `DELETE /futures/isolated/trade/stoploss` (clears fixed stop and trailing distance).
- `futures.isolated.remove_takeprofit()` method — maps to `DELETE /futures/isolated/trade/takeprofit`.
- `mode` field on `UpdateStoplossParams` (`"fixed"` | `"trailing"`, default `"fixed"`) — set a trailing stop via `update_stoploss` with `mode="trailing"` and `value` as a fractional distance.
- `stoploss_trailing_distance` field on the trade response model.

## [0.1.1] - 2026-06-02

### Added

- `sum_cash_in_margin` and `sum_cash_in_pl` fields on the trade response model.

## [0.1.0] - 2026-05-13

### Added

- `stream/v1` WebSocket client (`stream_v1` package, models, auth, public, subscription).
- `account.read_notifications()` method — maps to `PUT /account/notifications` (mark all as read).
- `examples/stream_v1.py` demonstrating WebSocket usage.

### Changed

- Package layout: `lnmarkets_sdk.rest_v3` → `lnmarkets_sdk.rest.v3`.
- Renamed `examples/basic.py` → `examples/rest_v3.py`.
- `examples/rest_v3.py`: take-profit update now opens a real isolated market trade and uses its ID instead of hardcoded UUID.

### Removed

- `AccountClient.withdraw_internal` (endpoint not present in api-rest-v3).
- `AccountClient.get_internal_deposits` (endpoint not present in api-rest-v3).
- `AccountClient.get_internal_withdrawals` (endpoint not present in api-rest-v3).
- Associated models: `WithdrawInternalParams`, `WithdrawInternalResponse`, `InternalDeposit`, `InternalWithdrawal`, `GetInternalDepositsParams`, `GetInternalWithdrawalsParams`.

### Fixed

- `examples/rest_v3.py`: `update_takeprofit` no longer hits hardcoded trade ID that returned `400 You do not own this trade`.
