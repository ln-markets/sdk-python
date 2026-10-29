# LN Markets SDK

[![CI](https://github.com/ln-markets/sdk-python/actions/workflows/check.yml/badge.svg)](https://github.com/ln-markets/sdk-python/actions/workflows/check.yml)

Python SDK for the LN Markets API. Ships two clients:

- **REST v3** (`lnmarkets_sdk.rest.v3`) — request/response API.
- **Stream v1** (`lnmarkets_sdk.stream.v1`) — JSON-RPC WebSocket with subscriptions.

## REST v3

For public endpoints, you can just do this:

```python
from lnmarkets_sdk.rest.v3.http.client import LNMClient
from lnmarkets_sdk.rest.v3.models.perp import PerpMarketKey
import asyncio

async with LNMClient() as client:
  markets = await client.get_markets()
  await asyncio.sleep(1)
  ticker = await client.perp.get_ticker(
      PerpMarketKey(instrument="inverse_perp", pair="btc_usd")
  )
```

Remember to sleep between requests, as the rate limit is 1 requests per second for public endpoints.

For endpoints that need authentication, you need to create an instance of the `LNMClient` class and provide your API credentials:

```python
from lnmarkets_sdk.rest.v3.http.client import APIAuthContext, APIClientConfig, LNMClient

config = APIClientConfig(
    authentication=APIAuthContext(
        key=your_key,
        secret=your_secret,
        passphrase=your_passphrase,
    ),
    network="mainnet",
    timeout=60.0,  # 60 second timeout (default is 30s)
    )

async with LNMClient(config) as client:
  account = await client.account.get_account()
```

For endpoints that requires input parameters, you can find the corresponding models in the `lnmarkets_sdk.rest.v3.models` module.

```python

from lnmarkets_sdk.rest.v3.http.client import APIAuthContext, APIClientConfig, LNMClient
from lnmarkets_sdk.rest.v3.models.account import GetLightningDepositsParams

config = APIClientConfig(
    authentication=APIAuthContext(
        key=your_key,
        secret=your_secret,
        passphrase=your_passphrase,
    ),
    network="mainnet",
    timeout=60.0,  # 60 second timeout (default is 30s)
    )

async with LNMClient(config) as client:
    deposits = await client.account.get_lightning_deposits(
        GetLightningDepositsParams(limit=5)
    )
```

### Perp markets

LN Markets has more than one perp market: the Bitcoin perp (`inverse_perp` + `btc_usd`) and quanto perps such as qGOLD (`quanto_perp` + `xau_usdt`). The `client.perp` methods take the market key (`instrument` + `pair`). `client.get_markets()` lists the markets you can use; it also lists the early-access markets your API key can access.

```python
from lnmarkets_sdk.rest.v3.models.perp import (
    GetPerpTradesParams,
    PerpOrder,
    PerpStoploss,
    PerpTradeParams,
    PerpUpdateTakeprofitParams,
)

GOLD = {"instrument": "quanto_perp", "pair": "xau_usdt"}

async with LNMClient(config) as client:
    trade = await client.perp.isolated.new_trade(
        PerpOrder(
            **GOLD,
            type="market",
            side="buy",
            margin=10_000,  # or quantity=..., in the market's unit (ounces for qGOLD)
            leverage=10,
            stoploss=PerpStoploss(mode="trailing", value=0.05),
        )
    )
    await client.perp.isolated.update_takeprofit(
        PerpUpdateTakeprofitParams(id=trade.id, value=5_000, **GOLD)
    )
    closed = await client.perp.isolated.close(PerpTradeParams(id=trade.id, **GOLD))

    # Reads without a market key cover every market.
    running = await client.perp.isolated.get_running_trades()

    # History reads use cursor pagination: pass `next_cursor` back as `cursor`.
    params = GetPerpTradesParams(**GOLD, limit=50)
    page = await client.perp.isolated.get_closed_trades(params)
    while page.next_cursor:
        params.cursor = page.next_cursor
        page = await client.perp.isolated.get_closed_trades(params)
```

The `client.futures` methods that have a `client.perp` replacement (ticker, candles, funding settlements and all isolated methods) are deprecated and raise a `DeprecationWarning`. They still work and trade BTC/USD only. To move, call the `client.perp` method with the same name and `instrument="inverse_perp", pair="btc_usd"`. Note that `PerpOrder.stoploss` is an object (`PerpStoploss(mode=..., value=...)`), not a number plus `stoploss_mode`.

Check our [REST example](./examples/rest_v3.py) for more details.

### Available Methods

🔒 = requires API credentials

```python
# Ping
client.ping()

# Markets
client.get_markets()

# Account 🔒
client.account.get_account()
client.account.get_bitcoin_address()
client.account.add_bitcoin_address()
client.account.deposit_lightning()
client.account.withdraw_lightning()
client.account.withdraw_on_chain()
client.account.get_lightning_deposits()
client.account.get_lightning_withdrawals()
client.account.get_on_chain_deposits()
client.account.get_on_chain_withdrawals()
client.account.read_notifications()

# Perp
client.perp.get_ticker()
client.perp.get_candles()
client.perp.get_funding_settlements()

# Perp Isolated 🔒
client.perp.isolated.new_trade()
client.perp.isolated.get_running_trades()
client.perp.isolated.get_open_trades()
client.perp.isolated.get_closed_trades()
client.perp.isolated.get_canceled_trades()
client.perp.isolated.close()
client.perp.isolated.cancel()
client.perp.isolated.cancel_all()
client.perp.isolated.add_margin()
client.perp.isolated.cash_in()
client.perp.isolated.update_stoploss()
client.perp.isolated.update_takeprofit()
client.perp.isolated.remove_stoploss()
client.perp.isolated.remove_takeprofit()
client.perp.isolated.get_funding_fees()

# Futures (BTC/USD only)
client.futures.get_ticker()               # deprecated, use client.perp
client.futures.get_leaderboard()
client.futures.get_candles()              # deprecated, use client.perp
client.futures.get_funding_settlements()  # deprecated, use client.perp

# Futures Isolated 🔒 (deprecated, use client.perp.isolated)
client.futures.isolated.new_trade()
client.futures.isolated.get_running_trades()
client.futures.isolated.get_open_trades()
client.futures.isolated.get_closed_trades()
client.futures.isolated.get_canceled_trades()
client.futures.isolated.close()
client.futures.isolated.cancel()
client.futures.isolated.cancel_all()
client.futures.isolated.add_margin()
client.futures.isolated.cash_in()
client.futures.isolated.update_stoploss()
client.futures.isolated.update_takeprofit()
client.futures.isolated.remove_stoploss()
client.futures.isolated.remove_takeprofit()
client.futures.isolated.get_funding_fees()

# Futures Cross 🔒
client.futures.cross.new_order()
client.futures.cross.get_position()
client.futures.cross.get_open_orders()
client.futures.cross.get_filled_orders()
client.futures.cross.close()
client.futures.cross.cancel()
client.futures.cross.cancel_all()
client.futures.cross.deposit()
client.futures.cross.withdraw()
client.futures.cross.set_leverage()
client.futures.cross.get_transfers()
client.futures.cross.get_funding_fees()

# Synthetic USD
client.synthetic_usd.get_best_price()
client.synthetic_usd.get_swaps()  # 🔒
client.synthetic_usd.new_swap()   # 🔒
```

## Stream v1

WebSocket JSON-RPC client. Connect, subscribe to topics, register event listeners.

Public stream:

```python
import asyncio
from lnmarkets_sdk.stream.v1 import StreamClientConfig, create_stream_client
from lnmarkets_sdk.stream.v1.models import SubscribeParams

async def main():
    config = StreamClientConfig(network="mainnet")
    client = create_stream_client(config)

    client.on(
        "futures/inverse/btc_usd/ticker",
        lambda data: print(data["lastPrice"]),
    )

    await client.connect()
    await client.subscription.subscribe(
        SubscribeParams(topics=["futures/inverse/btc_usd/ticker"]),
    )
    await asyncio.sleep(30)
    await client.close()

asyncio.run(main())
```

Authenticated stream (private topics: trades, orders, position, wallet):

```python
from lnmarkets_sdk.stream.v1 import StreamClientConfig, create_stream_client
from lnmarkets_sdk.stream.v1.models import AuthenticateParams, SubscribeParams

config = StreamClientConfig(
    network="mainnet",
    reconnect_enabled=True,
    reconnect_interval=5.0,
    max_reconnect_attempts=5,
)
client = create_stream_client(config)

await client.connect()
await client.auth.authenticate(
    AuthenticateParams(key=your_key, secret=your_secret, passphrase=your_passphrase),
)
await client.subscription.subscribe(
    SubscribeParams(topics=[
        "futures/inverse/btc_usd/isolated/trades",
        "wallet/deposit",
        "wallet/withdrawal",
    ]),
)
```

Server rate-limits to 10 messages/sec per socket — pace RPC calls accordingly.

Check our [Stream example](./examples/stream_v1.py) for full RPC + topic coverage.

### Available RPCs and Topics

🔒 = requires authentication

```python
# Public RPCs
client.public.hello()
client.public.ping()
client.public.time()

# Auth RPCs 🔒
client.auth.authenticate()
client.auth.whoami()

# Subscription RPCs
client.subscription.subscribe()
client.subscription.unsubscribe()
client.subscription.unsubscribe_all()

# Lifecycle events
client.on("open", ...)
client.on("close", ...)
client.on("error", ...)
client.on("reconnected", ...)

# Public topics
"announcements"
"futures/inverse/btc_usd/ticker"
"futures/inverse/btc_usd/lastPrice"
"futures/inverse/btc_usd/index"
"futures/inverse/btc_usd/buckets"
"futures/inverse/btc_usd/funding"
"futures/inverse/btc_usd/ohlc/1m"
"futures/inverse/btc_usd/ohlc/5m"

# Private topics 🔒
"futures/inverse/btc_usd/isolated/trades"
"futures/inverse/btc_usd/cross/orders"
"futures/inverse/btc_usd/cross/position"
"wallet/deposit"
"wallet/withdrawal"
```

## API Reference

- [REST](https://docs.lnmarkets.com/en/api)
- [STREAM](https://docs.lnmarkets.com/en/stream)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
