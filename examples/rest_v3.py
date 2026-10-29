"""REST v3 runnable example — public endpoints + optional authenticated flow.

Creds loaded from `.env` via `python-dotenv`.

Run:
    uv run examples/rest_v3.py                  # public-only, signet
    uv run examples/rest_v3.py --auth           # authenticated, signet
    uv run examples/rest_v3.py --mainnet
    uv run examples/rest_v3.py --mainnet --auth

Authenticated run reads creds by network:
    mainnet  -> MAINNET_API_KEY, MAINNET_API_SECRET, MAINNET_API_PASSPHRASE
    signet -> SIGNET_API_KEY, SIGNET_API_SECRET, SIGNET_API_PASSPHRASE
"""

import asyncio
import os
import sys
from pprint import pprint
from typing import Literal

from dotenv import load_dotenv

from lnmarkets_sdk.rest.v3.http.client import APIAuthContext, APIClientConfig, LNMClient
from lnmarkets_sdk.rest.v3.models.account import (
    GetLightningDepositsParams,
    GetNotificationsParams,
)
from lnmarkets_sdk.rest.v3.models.futures_cross import FuturesCrossOrderLimit
from lnmarkets_sdk.rest.v3.models.perp import (
    GetPerpCandlesParams,
    GetPerpFundingFeesParams,
    GetPerpFundingSettlementsParams,
    GetPerpTradesParams,
    PerpMarketFilter,
    PerpMarketKey,
    PerpOrder,
    PerpStoploss,
    PerpTradeParams,
    PerpUpdateStoplossParams,
    PerpUpdateTakeprofitParams,
)

Network = Literal["mainnet", "signet"]

load_dotenv()

BTC_USD = PerpMarketKey(instrument="inverse_perp", pair="btc_usd")


async def pick_market(client: LNMClient) -> PerpMarketKey:
    """Pick a perp market other than BTC/USD (e.g. qGOLD), else BTC/USD.

    Which markets you can trade depends on the network and on your API key.
    """
    for market in await client.get_markets():
        if market.instrument in ("inverse_perp", "quanto_perp") and (
            market.instrument,
            market.pair,
        ) != (BTC_USD.instrument, BTC_USD.pair):
            return PerpMarketKey(instrument=market.instrument, pair=market.pair)
    return BTC_USD


async def example_public_endpoints(network: Network):
    """Example: Make public requests without authentication."""
    print("\n" + "=" * 80)
    print(f"PUBLIC ENDPOINTS EXAMPLE ({network})")
    print("=" * 80)

    # Create client without authentication for public endpoints
    # The httpx.AsyncClient is created once and reuses connections
    async with LNMClient(APIClientConfig(network=network)) as client:
        # All these requests share the same connection pool
        print("\n🔄 Making multiple requests with connection reuse...")

        # List the markets
        markets = await client.get_markets()
        print("\n--- Markets ---")
        for market in markets:
            print(f"  {market.id} ({market.display_name}): {market.status}")

        # Get a perp ticker
        await asyncio.sleep(1)
        market = await pick_market(client)
        await asyncio.sleep(1)
        ticker = await client.perp.get_ticker(market)
        print(f"\n--- Perp Ticker ({market.instrument}:{market.pair}) ---")
        pprint(ticker.model_dump(), indent=2, width=100)

        # Get leaderboard
        await asyncio.sleep(1)
        leaderboard = await client.futures.get_leaderboard()
        print("\n--- Leaderboard (Top 3 Daily) ---")
        pprint(leaderboard.daily[:3], indent=2, width=100)

        # Get synthetic USD best price
        await asyncio.sleep(1)
        best_price = await client.synthetic_usd.get_best_price()
        print("\n--- Synthetic USD Best Price ---")
        pprint(best_price.model_dump(), indent=2)

        # Ping the API
        await asyncio.sleep(1)
        ping_response = await client.ping()
        print("\n--- Ping ---")
        print(f"Response: {ping_response}")

        # Get server time
        await asyncio.sleep(1)
        time_response = await client.time()
        print("\n--- Server Time ---")
        print(f"Response: {time_response}")

        # Get perp candles, two pages
        await asyncio.sleep(1)
        candles_params = GetPerpCandlesParams(
            **market.model_dump(), range="1h", limit=3
        )
        candles = await client.perp.get_candles(candles_params)
        print("\n--- Perp Candles (Last 3) ---")
        for candle in candles.data:
            print(
                f"Time: {candle.time}, OHLC: {candle.open}/{candle.high}/{candle.low}/{candle.close}"
            )
        if candles.next_cursor:
            # Pass `next_cursor` back as `cursor` to get the next page.
            await asyncio.sleep(1)
            candles_params.cursor = candles.next_cursor
            older = await client.perp.get_candles(candles_params)
            print(f"Next page starts at: {older.data[0].time if older.data else None}")

        # Get funding settlements
        await asyncio.sleep(1)
        funding_settlements = await client.perp.get_funding_settlements(
            GetPerpFundingSettlementsParams(**market.model_dump(), limit=5)
        )
        print("\n--- Funding Settlements (Last 5) ---")
        for settlement in funding_settlements.data[:3]:  # Show first 3
            print(
                f"Rate: {settlement.funding_rate}, "
                f"Quanto adjustment: {settlement.quanto_adjustment_rate}, "
                f"Price: {settlement.fixing_price}, Time: {settlement.time}"
            )


async def example_authenticated_endpoints(network: Network):
    """Example: Use authenticated endpoints with credentials."""
    print("\n" + "=" * 80)
    print(f"AUTHENTICATED ENDPOINTS EXAMPLE ({network})")
    print("=" * 80)

    prefix = network.upper()
    key = os.getenv(f"{prefix}_API_KEY")
    secret = os.getenv(f"{prefix}_API_KEY_SECRET")
    passphrase = os.getenv(f"{prefix}_API_KEY_PASSPHRASE")

    if not (key and secret and passphrase):
        print("\n⚠️  Skipping authenticated example:")
        print(
            f"    Please set {prefix}_API_KEY, {prefix}_API_KEY_SECRET, "
            f"and {prefix}_API_KEY_PASSPHRASE"
        )
        return

    # Create config with authentication and custom timeout
    config = APIClientConfig(
        authentication=APIAuthContext(
            key=key,
            secret=secret,
            passphrase=passphrase,
        ),
        network=network,
        timeout=60.0,  # 60 second timeout (default is 30s)
    )

    async with LNMClient(config) as client:
        print("\n🔐 Using authenticated endpoints with connection pooling...")

        # Get account info
        account = await client.account.get_account()
        print("\n--- Account Info ---")
        print(f"Username: {account.username}")
        print(f"Balance: {account.balance} sats")
        print(f"Synthetic USD Balance: {account.synthetic_usd_balance}")

        # Get Bitcoin address
        btc_address = await client.account.get_bitcoin_address()
        print("\n--- Bitcoin Deposit Address ---")
        print(f"Address: {btc_address.address}")

        # Get lightning deposits (last 5)
        deposits_response = await client.account.get_lightning_deposits(
            GetLightningDepositsParams(from_="1970-01-01T00:00:00.000Z", limit=5)
        )
        print(
            f"\n--- Recent Lightning Deposits (Last {len(deposits_response.data)}) ---"
        )
        for deposit in deposits_response.data:
            print(f"Deposits {deposit.amount} sats at {deposit.created_at}")

        # List current notifications. Notifications fire server-side on async
        # events (deposit settled, withdrawal processed, trade closed by SL/TP,
        # funding settlements, system announcements) — not synchronously from
        # the client. List may be empty on a fresh testnet account.
        await asyncio.sleep(1)
        notifs = await client.account.get_notifications(GetNotificationsParams(limit=5))
        unread = sum(1 for n in notifs.data if not n.read)
        print(f"\n--- Notifications (unread: {unread}/{len(notifs.data)}) ---")
        for n in notifs.data[:3]:
            print(f"  [{'x' if n.read else ' '}] {n.message}")

        # Mark all notifications as read (no-op if list is empty)
        await asyncio.sleep(1)
        await client.account.read_notifications()
        print("\n--- read_notifications() called ---")

        # Running trades of every perp market
        await asyncio.sleep(1)
        running_trades = await client.perp.isolated.get_running_trades()
        print("\n--- Running Isolated Trades (all markets) ---")
        print(f"Count: {len(running_trades)}")
        for trade in running_trades[:3]:  # Show first 3
            side = "LONG" if trade.side == "buy" else "SHORT"
            print(
                f"  {trade.instrument}:{trade.pair} {side} - Margin: {trade.margin} sats, "
                f"Leverage: {trade.leverage}x, PL: {trade.pl} sats"
            )

        # Open trades of one market
        await asyncio.sleep(1)
        market = await pick_market(client)
        open_trades = await client.perp.isolated.get_open_trades(
            PerpMarketFilter(**market.model_dump())
        )
        print(f"\n--- Open Isolated Trades on {market.pair} ---")
        for trade in open_trades[:3]:  # Show first 3
            side = "LONG" if trade.side == "buy" else "SHORT"
            print(f"  {side} - Price: {trade.price}, Quantity: {trade.quantity}")

        # Closed trades
        await asyncio.sleep(1)
        closed_trades = await client.perp.isolated.get_closed_trades(
            GetPerpTradesParams(limit=5)
        )
        print(f"\n--- Closed Isolated Trades (Last {len(closed_trades.data)}) ---")
        for trade in closed_trades.data[:3]:  # Show first 3
            side = "LONG" if trade.side == "buy" else "SHORT"
            print(f"  {trade.pair} {side} - PL: {trade.pl} sats")

        # Isolated funding fees
        await asyncio.sleep(1)
        isolated_fees = await client.perp.isolated.get_funding_fees(
            GetPerpFundingFeesParams(limit=5)
        )
        print(f"\n--- Isolated Funding Fees (Last {len(isolated_fees.data)}) ---")
        for fee in isolated_fees.data[:3]:  # Show first 3
            print(
                f"{fee.pair} Fee: {fee.fee} sats, "
                f"Quanto: {fee.quanto_adjustment_fee} sats, Time: {fee.time}"
            )

        # Get cross margin position
        try:
            position = await client.futures.cross.get_position()
            print("\n--- Cross Margin Position ---")
            print(f"Quantity: {position.quantity}")
            print(f"Margin: {position.margin} sats")
            print(f"Leverage: {position.leverage}x")
            print(f"Total PL: {position.total_pl} sats")
        except Exception as e:
            print(f"Error: {e}")

        # Open a new cross order
        try:
            print("\n--- Try to open a new cross order ---")
            order_params = FuturesCrossOrderLimit(
                type="limit",
                price=101000,
                quantity=10,
                side="sell",
                client_id="custom-ref-123",
            )
            new_order = await client.futures.cross.new_order(order_params)
            print(f"New order: {new_order}")
        except Exception as e:
            print(f"Error: {e}")

        print(f"\n --- Trade on {market.instrument}:{market.pair} ---")
        try:
            # Size the trade by margin: the quantity unit depends on the market
            # (USD for BTC/USD, ounces for qGOLD, ...).
            opened = await client.perp.isolated.new_trade(
                PerpOrder(
                    **market.model_dump(),
                    type="market",
                    side="buy",
                    margin=10_000,
                    leverage=10,
                )
            )
            print(f"Opened trade ID: {opened.id}, quantity: {opened.quantity}")
            trade = PerpTradeParams(id=opened.id, **market.model_dump())

            # Take profit above entry, stop loss between liquidation and entry.
            await asyncio.sleep(1)
            updated = await client.perp.isolated.update_takeprofit(
                PerpUpdateTakeprofitParams(
                    **trade.model_dump(), value=round(opened.price * 1.5)
                )
            )
            print(f"Take profit: {updated.takeprofit}")

            await asyncio.sleep(1)
            updated = await client.perp.isolated.update_stoploss(
                PerpUpdateStoplossParams(
                    **trade.model_dump(),
                    stoploss=PerpStoploss(
                        mode="fixed",
                        value=round((opened.price + opened.liquidation) / 2),
                    ),
                )
            )
            print(f"Stop loss: {updated.stoploss}")

            # Switch to a trailing stop: `value` is a fraction of price, not a
            # price. It is capped by liquidation (~1/leverage).
            await asyncio.sleep(1)
            trailing = await client.perp.isolated.update_stoploss(
                PerpUpdateStoplossParams(
                    **trade.model_dump(),
                    stoploss=PerpStoploss(mode="trailing", value=0.05),
                )
            )
            print(f"Trailing distance: {trailing.stoploss_trailing_distance}")

            # Remove the stop loss (fixed and trailing) and the take profit.
            await asyncio.sleep(1)
            await client.perp.isolated.remove_stoploss(trade)
            await asyncio.sleep(1)
            await client.perp.isolated.remove_takeprofit(trade)

            await asyncio.sleep(1)
            closed = await client.perp.isolated.close(trade)
            print(f"Closed trade {closed.id} - PL: {closed.pl} sats")
        except Exception as e:
            print(f"Error: {e}")


async def main():
    """Run all examples."""
    network: Network = "mainnet" if "--mainnet" in sys.argv else "signet"
    want_auth = "--auth" in sys.argv

    print("\n" + "=" * 80)
    print(f"LN MARKETS V3 CLIENT EXAMPLES (network={network}, auth={want_auth})")
    print("=" * 80)

    await example_public_endpoints(network)
    if want_auth:
        await example_authenticated_endpoints(network)

    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
