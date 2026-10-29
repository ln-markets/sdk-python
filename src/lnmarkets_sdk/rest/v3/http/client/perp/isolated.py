from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lnmarkets_sdk.rest.v3.http.client import LNMClient

from lnmarkets_sdk.rest.v3.models.perp import (
    GetPerpFundingFeesParams,
    GetPerpTradesParams,
    PerpAddMarginParams,
    PerpCanceledTrade,
    PerpCashInParams,
    PerpClosedTrade,
    PerpFundingFee,
    PerpMarketFilter,
    PerpMarketKey,
    PerpOpenTrade,
    PerpOrder,
    PerpPaginatedResponse,
    PerpRunningTrade,
    PerpRunningTradeRead,
    PerpTradeParams,
    PerpUpdateStoplossParams,
    PerpUpdateTakeprofitParams,
)


class PerpIsolatedClient:
    """Client for isolated margin perp endpoints (`/v3/perp/isolated`)."""

    def __init__(self, client: "LNMClient"):
        self._client = client

    async def new_trade(self, params: PerpOrder) -> PerpOpenTrade | PerpRunningTrade:
        """
        Open a new isolated trade on a perp market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpOrder, PerpStoploss

        async with LNMClient(config) as client:
            params = PerpOrder(
                instrument="quanto_perp",
                pair="xau_usdt",
                type="market",
                side="buy",
                margin=10_000,  # or quantity=..., in the market's quantity unit
                leverage=10,
                stoploss=PerpStoploss(mode="trailing", value=0.05),  # optional
            )
            trade = await client.perp.isolated.new_trade(params)
            print(f"Trade ID: {trade.id}")
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trade",
            params=params,
            credentials=True,
            response_model=PerpOpenTrade | PerpRunningTrade,
        )

    async def cancel(self, params: PerpTradeParams):
        """
        Cancel an open trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpTradeParams

        async with LNMClient(config) as client:
            params = PerpTradeParams(id=trade_id, instrument="quanto_perp", pair="xau_usdt")
            canceled = await client.perp.isolated.cancel(params)
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trade/cancel",
            params=params,
            credentials=True,
            response_model=PerpCanceledTrade,
        )

    async def cancel_all(self, params: PerpMarketKey):
        """
        Cancel all open trades of a perp market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpMarketKey

        async with LNMClient(config) as client:
            canceled = await client.perp.isolated.cancel_all(
                PerpMarketKey(instrument="quanto_perp", pair="xau_usdt")
            )
            print(f"Canceled {len(canceled)} trades")
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trades/cancel-all",
            params=params,
            credentials=True,
            response_model=list[PerpCanceledTrade],
        )

    async def close(self, params: PerpTradeParams):
        """
        Close a running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpTradeParams

        async with LNMClient(config) as client:
            params = PerpTradeParams(id=trade_id, instrument="quanto_perp", pair="xau_usdt")
            closed = await client.perp.isolated.close(params)
            print(f"P&L: {closed.pl}")
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trade/close",
            params=params,
            credentials=True,
            response_model=PerpClosedTrade,
        )

    async def add_margin(self, params: PerpAddMarginParams):
        """
        Add margin to a running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpAddMarginParams

        async with LNMClient(config) as client:
            params = PerpAddMarginParams(
                id=trade_id, amount=10_000, instrument="quanto_perp", pair="xau_usdt"
            )
            updated = await client.perp.isolated.add_margin(params)
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trade/add-margin",
            params=params,
            credentials=True,
            response_model=PerpRunningTrade,
        )

    async def cash_in(self, params: PerpCashInParams):
        """
        Cash in from a running trade (P&L first, then margin).

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpCashInParams

        async with LNMClient(config) as client:
            params = PerpCashInParams(
                id=trade_id, amount=1_000, instrument="quanto_perp", pair="xau_usdt"
            )
            updated = await client.perp.isolated.cash_in(params)
        ```
        """
        return await self._client.request(
            "POST",
            "/perp/isolated/trade/cash-in",
            params=params,
            credentials=True,
            response_model=PerpRunningTrade,
        )

    async def update_stoploss(
        self, params: PerpUpdateStoplossParams
    ) -> PerpOpenTrade | PerpRunningTrade:
        """
        Update the stop loss of an open or running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpStoploss, PerpUpdateStoplossParams

        async with LNMClient(config) as client:
            params = PerpUpdateStoplossParams(
                id=trade_id,
                stoploss=PerpStoploss(mode="fixed", value=2_000),
                instrument="quanto_perp",
                pair="xau_usdt",
            )
            updated = await client.perp.isolated.update_stoploss(params)
        ```
        """
        return await self._client.request(
            "PUT",
            "/perp/isolated/trade/stoploss",
            params=params,
            credentials=True,
            response_model=PerpOpenTrade | PerpRunningTrade,
        )

    async def update_takeprofit(
        self, params: PerpUpdateTakeprofitParams
    ) -> PerpOpenTrade | PerpRunningTrade:
        """
        Update the take profit of an open or running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpUpdateTakeprofitParams

        async with LNMClient(config) as client:
            params = PerpUpdateTakeprofitParams(
                id=trade_id, value=3_000, instrument="quanto_perp", pair="xau_usdt"
            )
            updated = await client.perp.isolated.update_takeprofit(params)
        ```
        """
        return await self._client.request(
            "PUT",
            "/perp/isolated/trade/takeprofit",
            params=params,
            credentials=True,
            response_model=PerpOpenTrade | PerpRunningTrade,
        )

    async def remove_stoploss(
        self, params: PerpTradeParams
    ) -> PerpOpenTrade | PerpRunningTrade:
        """
        Remove the stop loss (fixed and trailing) of an open or running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpTradeParams

        async with LNMClient(config) as client:
            params = PerpTradeParams(id=trade_id, instrument="quanto_perp", pair="xau_usdt")
            updated = await client.perp.isolated.remove_stoploss(params)
        ```
        """
        return await self._client.request(
            "DELETE",
            "/perp/isolated/trade/stoploss",
            params=params,
            credentials=True,
            response_model=PerpOpenTrade | PerpRunningTrade,
        )

    async def remove_takeprofit(
        self, params: PerpTradeParams
    ) -> PerpOpenTrade | PerpRunningTrade:
        """
        Remove the take profit of an open or running trade.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpTradeParams

        async with LNMClient(config) as client:
            params = PerpTradeParams(id=trade_id, instrument="quanto_perp", pair="xau_usdt")
            updated = await client.perp.isolated.remove_takeprofit(params)
        ```
        """
        return await self._client.request(
            "DELETE",
            "/perp/isolated/trade/takeprofit",
            params=params,
            credentials=True,
            response_model=PerpOpenTrade | PerpRunningTrade,
        )

    async def get_open_trades(self, params: PerpMarketFilter | None = None):
        """
        Get the open trades of every perp market, or of one market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import PerpMarketFilter

        async with LNMClient(config) as client:
            all_markets = await client.perp.isolated.get_open_trades()
            gold = await client.perp.isolated.get_open_trades(
                PerpMarketFilter(instrument="quanto_perp", pair="xau_usdt")
            )
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/isolated/trades/open",
            params=params,
            credentials=True,
            response_model=list[PerpOpenTrade],
        )

    async def get_running_trades(self, params: PerpMarketFilter | None = None):
        """
        Get the running trades of every perp market, or of one market.

        `pl` is the unrealized P&L at the Mark price.

        Example:
        ```python
        async with LNMClient(config) as client:
            trades = await client.perp.isolated.get_running_trades()
            for trade in trades:
                print(f"{trade.instrument}:{trade.pair} {trade.id} P&L: {trade.pl}")
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/isolated/trades/running",
            params=params,
            credentials=True,
            response_model=list[PerpRunningTradeRead],
        )

    async def get_closed_trades(self, params: GetPerpTradesParams | None = None):
        """
        Get the closed trades of every perp market, or of one market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import GetPerpTradesParams

        async with LNMClient(config) as client:
            params = GetPerpTradesParams(instrument="quanto_perp", pair="xau_usdt", limit=10)
            response = await client.perp.isolated.get_closed_trades(params)
            if response.next_cursor:
                params.cursor = response.next_cursor
                next_page = await client.perp.isolated.get_closed_trades(params)
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/isolated/trades/closed",
            params=params,
            credentials=True,
            response_model=PerpPaginatedResponse[PerpClosedTrade],
        )

    async def get_canceled_trades(self, params: GetPerpTradesParams | None = None):
        """
        Get the canceled trades of every perp market, or of one market.

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import GetPerpTradesParams

        async with LNMClient(config) as client:
            params = GetPerpTradesParams(limit=10)
            response = await client.perp.isolated.get_canceled_trades(params)
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/isolated/trades/canceled",
            params=params,
            credentials=True,
            response_model=PerpPaginatedResponse[PerpCanceledTrade],
        )

    async def get_funding_fees(self, params: GetPerpFundingFeesParams | None = None):
        """
        Get the funding fees paid by isolated trades.

        Filter by market (`instrument` + `pair`) or by trade (`trade_id`).

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.models.perp import GetPerpFundingFeesParams

        async with LNMClient(config) as client:
            params = GetPerpFundingFeesParams(trade_id=trade_id, limit=10)
            response = await client.perp.isolated.get_funding_fees(params)
            for fee in response.data:
                print(f"Fee: {fee.fee}, Quanto: {fee.quanto_adjustment_fee}")
        ```
        """
        return await self._client.request(
            "GET",
            "/perp/isolated/funding-fees",
            params=params,
            credentials=True,
            response_model=PerpPaginatedResponse[PerpFundingFee],
        )
