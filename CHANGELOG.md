# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
