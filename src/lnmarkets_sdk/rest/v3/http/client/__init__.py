from collections.abc import Mapping
from types import UnionType

from pydantic import BaseModel

from lnmarkets_sdk.rest.v3._internal import BaseClient
from lnmarkets_sdk.rest.v3._internal.models import (
    APIAuthContext,
    APIClientConfig,
    APIMethod,
)
from lnmarkets_sdk.rest.v3._internal.utils import get_hostname, parse_response
from lnmarkets_sdk.rest.v3.models.markets import Market

from .account import AccountClient
from .futures import FuturesClient
from .perp import PerpClient
from .synthetic_usd import SyntheticUSDClient


class LNMClient:
    """
    Main client for LN Markets API v3.

    This client provides a convenient interface to all LN Markets endpoints
    organized by category. Create an instance and use it within an async
    context manager.
    """

    def __init__(self, config: APIClientConfig | None = None):
        """
        Initialize the LN Markets client.

        Args:
            config: Client configuration

        Example:
        ```python
        from lnmarkets_sdk.rest.v3.http.client import LNMClient, APIClientConfig, APIAuthContext
        from lnmarkets_sdk.rest.v3.models.perp import PerpMarketKey, PerpOrder

        config = APIClientConfig(
            authentication=APIAuthContext(
                key="your-key",
                secret="your-secret",
                passphrase="your-passphrase",
            ),
            network="mainnet",
            timeout=30,
        )

        async with LNMClient(config) as client:
            # Get account info
            account = await client.account.get_account()

            # Get market ticker
            ticker = await client.perp.get_ticker(
                PerpMarketKey(instrument="inverse_perp", pair="btc_usd")
            )

            # Place a perp order
            params = PerpOrder(
                instrument="inverse_perp",
                pair="btc_usd",
                type="limit",  # limit order
                side="buy",  # buy
                price=100_000,
                quantity=1,
                leverage=100,
            )
            order = await client.perp.isolated.new_trade(params)
        ```
        """
        if config is None:
            config = APIClientConfig()

        auth = config.authentication
        hostname = config.hostname or get_hostname(config.network)
        base_url = f"https://{hostname}/v3"

        self._base_client = BaseClient(
            base_url=base_url,
            timeout=config.timeout,
            auth=auth,
            custom_headers=config.custom_headers,
            max_retries=config.max_retries,
            retry_base_delay=config.retry_base_delay,
            retry_max_delay=config.retry_max_delay,
        )

        self.account = AccountClient(self)
        self.futures = FuturesClient(self)
        self.perp = PerpClient(self)
        self.synthetic_usd = SyntheticUSDClient(self)

    async def __aenter__(self) -> "LNMClient":
        """Enter async context manager."""
        await self._base_client.__aenter__()
        return self

    async def __aexit__(self, *args: object) -> None:
        """Exit async context manager."""
        await self._base_client.__aexit__(*args)

    @property
    def authenticated(self) -> bool:
        """Whether the client has API credentials."""
        return self._base_client.auth is not None

    async def request[T](
        self,
        method: APIMethod,
        path: str,
        params: BaseModel | Mapping[str, object] | None = None,
        credentials: bool = False,
        response_model: type[T] | UnionType | None = None,
    ) -> T:
        """
        Make an HTTP request to the API with automatic validation.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Request parameters (Pydantic model or dict)
            credentials: Whether to include authentication
            response_model: Optional Pydantic model to validate response

        Returns:
            Validated response model or dict

        Raises:
            APIException: For API errors
            APIHTTPException: For HTTP errors
            APIValidationException: For validation errors
        """
        response = await self._base_client.request(method, path, params, credentials)
        return parse_response(response, response_model)

    async def request_raw(
        self,
        method: APIMethod,
        path: str,
        params: BaseModel | Mapping[str, object] | None = None,
        credentials: bool = False,
    ) -> str:
        """Make an HTTP request and return raw text response."""
        response = await self._base_client.request(method, path, params, credentials)
        response.raise_for_status()
        return response.text

    async def ping(self) -> str:
        """Ping the API to check connectivity."""
        return await self.request_raw("GET", "/ping", credentials=False)

    async def time(self) -> str:
        """
        Get server time.

        Example:
        ```python
        async with LNMClient(config) as client:
            time_response = await client.time()
            print(f"Server time: {time_response}")
        ```
        """
        return await self.request_raw("GET", "/time", credentials=False)

    async def get_markets(self):
        """
        List the markets: the released ones, plus the ones the API key can access.

        Example:
        ```python
        async with LNMClient(config) as client:
            markets = await client.get_markets()
            for market in markets:
                print(f"{market.instrument} {market.pair}: {market.display_name}")
        ```
        """
        return await self.request(
            "GET",
            "/markets",
            credentials=self.authenticated,
            response_model=list[Market],
        )


__all__ = ["APIAuthContext", "APIClientConfig", "LNMClient"]
