from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lnmarkets_sdk.rest.v3.http.client import LNMClient

from lnmarkets_sdk.rest.v3.models.perp import (
    GetPerpCandlesParams,
    GetPerpFundingSettlementsParams,
    PerpCandles,
    PerpFundingSettlements,
    PerpMarketKey,
    PerpTicker,
)

from .isolated import PerpIsolatedClient


class PerpClient:
    """Client for perp market endpoints (`/v3/perp`).

    Every method takes the market key (`instrument` + `pair`), e.g.
    `inverse_perp` + `btc_usd` for the Bitcoin perp or `quanto_perp` +
    `xau_usdt` for the gold quanto perp. List the markets with
    `client.get_markets()`.
    """

    def __init__(self, client: "LNMClient"):
        self._client = client
        self.isolated = PerpIsolatedClient(client)

    async def get_ticker(self, params: PerpMarketKey):
        """
        Get the ticker of a perp market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpMarketKey

        async with LNMClient(config) as client:
            ticker = await client.perp.get_ticker(
                PerpMarketKey(instrument="quanto_perp", pair="xau_usdt")
            )
            print(f"Mark: {ticker.mark}, Funding Rate: {ticker.funding_rate}")
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/ticker",
            params=params,
            credentials=self._client.authenticated,
            response_model=PerpTicker,
        )

    async def get_candles(self, params: GetPerpCandlesParams):
        """
        Get OHLC candles of a perp market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import GetPerpCandlesParams

        async with LNMClient(config) as client:
            params = GetPerpCandlesParams(
                instrument="quanto_perp", pair="xau_usdt", range="1h", limit=100
            )
            response = await client.perp.get_candles(params)
            for candle in response.data:
                print(f"Time: {candle.time}, Close: {candle.close}")
            if response.next_cursor:
                params.cursor = response.next_cursor
                next_page = await client.perp.get_candles(params)
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/candles",
            params=params,
            credentials=self._client.authenticated,
            response_model=PerpCandles,
        )

    async def get_funding_settlements(self, params: GetPerpFundingSettlementsParams):
        """
        Get the funding settlement history of a perp market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import GetPerpFundingSettlementsParams

        async with LNMClient(config) as client:
            params = GetPerpFundingSettlementsParams(
                instrument="quanto_perp", pair="xau_usdt", limit=10
            )
            response = await client.perp.get_funding_settlements(params)
            for settlement in response.data:
                print(f"Rate: {settlement.funding_rate}")
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/funding-settlements",
            params=params,
            credentials=self._client.authenticated,
            response_model=PerpFundingSettlements,
        )
