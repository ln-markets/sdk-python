"""Unit tests for request transport and param serialization (no network).

Each test drives a real client method against a mocked HTTP transport and
asserts how the request goes out on the wire: the HTTP method, path, and
whether params land in the query string (GET/DELETE) or a JSON body (POST/PUT).
"""

import hashlib
import hmac
import json
from base64 import b64encode
from urllib.parse import urlencode

import pytest
from pydantic import ValidationError
from pytest_httpx import HTTPXMock

from lnmarkets_sdk.rest.v3._internal.models import APIException
from lnmarkets_sdk.rest.v3._internal.utils import prepare_params
from lnmarkets_sdk.rest.v3.http.client import (
    APIAuthContext,
    APIClientConfig,
    LNMClient,
)
from lnmarkets_sdk.rest.v3.models.futures_isolated import (
    FuturesOrder,
    GetClosedTradesParams,
    RemoveStoplossParams,
    RemoveTakeprofitParams,
    UpdateStoplossParams,
)
from lnmarkets_sdk.rest.v3.models.perp import (
    GetPerpTradesParams,
    PerpCursor,
    PerpMarketFilter,
    PerpMarketKey,
    PerpOpenTrade,
    PerpOrder,
    PerpRunningTrade,
    PerpStoploss,
    PerpTradeParams,
    PerpUpdateStoplossParams,
)

TRADE_ID = "d0b9f9a0-4f6e-4a5a-8b7a-7f0f5f9a8a1e"
SECRET = "test-secret"


def _auth_config() -> APIClientConfig:
    return APIClientConfig(
        network="signet",
        authentication=APIAuthContext(
            key="test-key",
            secret=SECRET,
            passphrase="test-passphrase",
        ),
    )


def _retry_config(max_retries: int = 2) -> APIClientConfig:
    """Auth config with tiny backoff delays so retry tests run fast."""
    return APIClientConfig(
        network="signet",
        authentication=APIAuthContext(
            key="test-key",
            secret=SECRET,
            passphrase="test-passphrase",
        ),
        max_retries=max_retries,
        retry_base_delay=0.01,
        retry_max_delay=0.02,
    )


def _no_wait_client(config: APIClientConfig) -> LNMClient:
    """Build a client whose backoff sleeps for zero seconds (keeps tests fast)."""
    client = LNMClient(config)
    client._base_client._backoff = lambda _rs: 0.0  # type: ignore[assignment]
    return client


def _error_body(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def _running_trade_payload() -> dict[str, object]:
    """Full open-or-running trade response (camelCase, as the API returns it)."""
    return {
        "id": TRADE_ID,
        "type": "market",
        "side": "buy",
        "openingFee": 0,
        "closingFee": 0,
        "maintenanceMargin": 100,
        "quantity": 1,
        "margin": 1000,
        "leverage": 10,
        "price": 100_000,
        "liquidation": 90_000,
        "stoploss": 0,
        "stoplossTrailingDistance": 0.1,
        "takeprofit": 0,
        "exitPrice": None,
        "pl": 0,
        "createdAt": "2026-01-01T00:00:00.000Z",
        "filledAt": "2026-01-01T00:00:01.000Z",
        "closedAt": None,
        "entryPrice": 100_000,
        "entryMargin": 1000,
        "open": False,
        "running": True,
        "canceled": False,
        "closed": False,
        "sumFundingFees": 0,
        "sumCashInPl": 0,
        "sumCashInMargin": 0,
        "clientId": None,
    }


def test_update_stoploss_params_serialize_mode() -> None:
    # Mode defaults to "fixed" when omitted.
    fixed = prepare_params(UpdateStoplossParams(id=TRADE_ID, value=50_000))
    assert fixed == {"id": TRADE_ID, "value": 50_000, "mode": "fixed"}

    # Trailing mode carries a fractional distance as `value`.
    trailing = prepare_params(
        UpdateStoplossParams(id=TRADE_ID, value=0.1, mode="trailing")
    )
    assert trailing is not None
    assert trailing["mode"] == "trailing"
    assert trailing["value"] == 0.1


async def test_get_running_trades_issues_plain_get(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=[])

    async with LNMClient(_auth_config()) as client:
        await client.futures.isolated.get_running_trades()

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/v3/futures/isolated/trades/running"
    assert request.url.query == b""
    assert request.read() == b""


async def test_get_closed_trades_sends_query_params(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json={"data": [], "nextCursor": None})

    async with LNMClient(_auth_config()) as client:
        await client.futures.isolated.get_closed_trades(GetClosedTradesParams(limit=10))

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "GET"
    assert request.url.path == "/v3/futures/isolated/trades/closed"
    # Params go in the query string, not a body.
    assert request.url.params["limit"] == "10"
    assert request.read() == b""


async def test_new_trade_posts_json_body(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        await client.futures.isolated.new_trade(
            FuturesOrder(type="market", side="buy", quantity=1, leverage=10)
        )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/v3/futures/isolated/trade"
    assert request.url.query == b""
    # Params go in the JSON body.
    assert request.headers["content-type"] == "application/json"
    body = json.loads(request.read())
    assert body["type"] == "market"
    assert body["side"] == "buy"


async def test_update_stoploss_trailing_puts_json_body(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        await client.futures.isolated.update_stoploss(
            UpdateStoplossParams(id=TRADE_ID, value=0.1, mode="trailing")
        )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "PUT"
    assert request.url.path == "/v3/futures/isolated/trade/stoploss"
    body = json.loads(request.read())
    assert body == {"id": TRADE_ID, "value": 0.1, "mode": "trailing"}


async def test_remove_stoploss_uses_delete_with_query_params(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(json=_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        result = await client.futures.isolated.remove_stoploss(
            RemoveStoplossParams(id=TRADE_ID)
        )

    # Response parses into the model, including the new trailing-distance field.
    assert str(result.id) == TRADE_ID
    assert result.stoploss_trailing_distance == 0.1

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    # `id` travels in the query string, not the body.
    assert request.url.params["id"] == TRADE_ID
    assert request.read() == b""

    # Signature is signed over the query string (server uses `data = body ?? url.search`).
    query = f"?{urlencode({'id': TRADE_ID})}"
    timestamp = request.headers["lnm-access-timestamp"]
    payload = f"{timestamp}delete/v3/futures/isolated/trade/stoploss{query}"
    expected = b64encode(
        hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    ).decode()
    assert request.headers["lnm-access-signature"] == expected


async def test_remove_takeprofit_uses_delete_with_query_params(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(json=_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        await client.futures.isolated.remove_takeprofit(
            RemoveTakeprofitParams(id=TRADE_ID)
        )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    assert request.url.path == "/v3/futures/isolated/trade/takeprofit"
    assert request.url.params["id"] == TRADE_ID
    assert request.read() == b""


async def test_retries_on_503_then_succeeds(httpx_mock: HTTPXMock) -> None:
    # First call flaps with the "Trading engine temporarily unavailable" 503,
    # the retry then succeeds.
    httpx_mock.add_response(
        status_code=503,
        json=_error_body(
            "SERVICE_UNAVAILABLE", "Trading engine is temporarily unavailable"
        ),
    )
    httpx_mock.add_response(json=[])

    async with _no_wait_client(_retry_config()) as client:
        result = await client.futures.cross.cancel_all()

    assert result == []
    # Two requests went out: the failed attempt and the successful retry.
    assert len(httpx_mock.get_requests()) == 2


async def test_retries_exhausted_raises_api_exception(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        status_code=503,
        json=_error_body(
            "SERVICE_UNAVAILABLE", "Trading engine is temporarily unavailable"
        ),
        is_reusable=True,
    )

    with pytest.raises(APIException, match="Trading engine is temporarily unavailable"):
        async with _no_wait_client(_retry_config(max_retries=2)) as client:
            await client.futures.cross.cancel_all()

    # Initial attempt + 2 retries.
    assert len(httpx_mock.get_requests()) == 3


async def test_retry_re_signs_each_attempt(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        status_code=503,
        json=_error_body("SERVICE_UNAVAILABLE", "unavailable"),
    )
    httpx_mock.add_response(json=[])

    async with _no_wait_client(_retry_config()) as client:
        await client.futures.cross.cancel_all()

    requests = httpx_mock.get_requests()
    assert len(requests) == 2
    # Every attempt carries a freshly built (re-signed) auth header.
    for req in requests:
        assert req.headers.get("lnm-access-signature")
        assert req.headers.get("lnm-access-timestamp")


async def test_retries_on_429_rate_limit(httpx_mock: HTTPXMock) -> None:
    # 429 is retried; a Retry-After header is honored by the wait strategy.
    httpx_mock.add_response(
        status_code=429,
        headers={"Retry-After": "0"},
        json=_error_body("TOO_MANY_REQUESTS", "rate limited"),
    )
    httpx_mock.add_response(json=[])

    async with _no_wait_client(_retry_config()) as client:
        result = await client.futures.cross.cancel_all()

    assert result == []
    assert len(httpx_mock.get_requests()) == 2


async def test_non_retryable_status_is_not_retried(httpx_mock: HTTPXMock) -> None:
    # A 400 is a client error: raise immediately, no retry.
    httpx_mock.add_response(
        status_code=400,
        json=_error_body("BAD_REQUEST", "invalid params"),
    )

    with pytest.raises(APIException, match="invalid params"):
        async with _no_wait_client(_retry_config()) as client:
            await client.futures.cross.cancel_all()

    assert len(httpx_mock.get_requests()) == 1


async def test_max_retries_zero_disables_retry(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        status_code=503,
        json=_error_body("SERVICE_UNAVAILABLE", "unavailable"),
    )

    with pytest.raises(APIException, match="unavailable"):
        async with _no_wait_client(_retry_config(max_retries=0)) as client:
            await client.futures.cross.cancel_all()

    assert len(httpx_mock.get_requests()) == 1


GOLD = {"instrument": "quanto_perp", "pair": "xau_usdt"}


def _perp_running_trade_payload() -> dict[str, object]:
    return {
        **_running_trade_payload(),
        **GOLD,
        "entryNotionalUsd": 4_000,
        "exitNotionalUsd": None,
        "entryBtcPrice": 100_000,
        "sumQuantoAdjustmentFees": 0,
    }


def _signature(method: str, path: str, data: str, timestamp: str) -> str:
    payload = f"{timestamp}{method}{path}{data}"
    return b64encode(
        hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    ).decode()


async def test_perp_new_trade_posts_market_key_and_stoploss(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(json=_perp_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        trade = await client.perp.isolated.new_trade(
            PerpOrder(
                **GOLD,
                type="market",
                side="buy",
                margin=10_000,
                leverage=10,
                stoploss=PerpStoploss(mode="trailing", value=0.05),
            )
        )

    assert isinstance(trade, PerpRunningTrade)
    assert trade.pair == "xau_usdt"

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "POST"
    assert request.url.path == "/v3/perp/isolated/trade"
    assert json.loads(request.read()) == {
        **GOLD,
        "leverage": 10,
        "side": "buy",
        "type": "market",
        "margin": 10_000,
        "stoploss": {"mode": "trailing", "value": 0.05},
    }


async def test_perp_open_trade_parses_as_open(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            **_perp_running_trade_payload(),
            "type": "limit",
            "running": False,
            "open": True,
            "filledAt": None,
        }
    )

    async with LNMClient(_auth_config()) as client:
        trade = await client.perp.isolated.new_trade(
            PerpOrder(
                **GOLD, type="limit", side="buy", price=2_000, quantity=1, leverage=10
            )
        )

    assert isinstance(trade, PerpOpenTrade)


async def test_perp_closed_trades_flatten_cursor_in_signed_query(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(json={"data": [], "nextCursor": None})
    cursor = PerpCursor(value="2026-01-01T00:00:00.000Z", id=TRADE_ID)

    async with LNMClient(_auth_config()) as client:
        await client.perp.isolated.get_closed_trades(
            GetPerpTradesParams(**GOLD, limit=10, cursor=cursor)
        )

    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/v3/perp/isolated/trades/closed"
    assert request.url.params["cursor[value]"] == "2026-01-01T00:00:00.000Z"
    assert request.url.params["cursor[id]"] == TRADE_ID
    assert request.url.params["instrument"] == "quanto_perp"
    assert "cursor" not in request.url.params

    # The server signs over `url.search`, so the signature must match the query sent.
    query = f"?{request.url.query.decode()}"
    timestamp = request.headers["lnm-access-timestamp"]
    expected = _signature("get", "/v3/perp/isolated/trades/closed", query, timestamp)
    assert request.headers["lnm-access-signature"] == expected


async def test_perp_closed_trades_parse_next_cursor(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        json={
            "data": [],
            "nextCursor": {"value": "2026-01-01T00:00:00.000Z", "id": TRADE_ID},
        }
    )

    async with LNMClient(_auth_config()) as client:
        page = await client.perp.isolated.get_closed_trades()

    assert page.next_cursor == PerpCursor(value="2026-01-01T00:00:00.000Z", id=TRADE_ID)


async def test_perp_remove_stoploss_sends_market_key_in_query(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(json=_perp_running_trade_payload())

    async with LNMClient(_auth_config()) as client:
        await client.perp.isolated.remove_stoploss(PerpTradeParams(id=TRADE_ID, **GOLD))

    request = httpx_mock.get_request()
    assert request is not None
    assert request.method == "DELETE"
    assert request.url.path == "/v3/perp/isolated/trade/stoploss"
    assert dict(request.url.params) == {"id": TRADE_ID, **GOLD}
    assert request.read() == b""


async def test_perp_get_ticker_is_public_without_credentials(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(
        json={
            **GOLD,
            "time": "2026-01-01T00:00:00.000Z",
            "mark": 2_000,
            "lastPrice": 2_001,
            "volume24h": 1_000_000,
            "prices": [],
            "fundingRate": 0.0001,
            "fundingTime": "2026-01-01T08:00:00.000Z",
            "quantoAdjustmentRate": 0.00005,
            "exchangesWeights": {"binance": 1},
        }
    )

    async with LNMClient(APIClientConfig(network="signet")) as client:
        ticker = await client.perp.get_ticker(PerpMarketKey(**GOLD))

    assert ticker.mark == 2_000
    assert ticker.quanto_adjustment_rate == 0.00005
    assert ticker.volume_24h == 1_000_000

    request = httpx_mock.get_request()
    assert request is not None
    assert dict(request.url.params) == GOLD
    assert "lnm-access-key" not in request.headers


async def test_perp_public_routes_sign_when_credentials_are_set(
    httpx_mock: HTTPXMock,
) -> None:
    # Early-access markets are only served to an API key that can access them.
    httpx_mock.add_response(json=[])

    async with LNMClient(_auth_config()) as client:
        markets = await client.get_markets()

    assert markets == []
    request = httpx_mock.get_request()
    assert request is not None
    assert request.url.path == "/v3/markets"
    assert request.headers["lnm-access-key"] == "test-key"


def test_perp_market_filter_needs_both_keys() -> None:
    with pytest.raises(ValidationError):
        PerpMarketFilter(instrument="quanto_perp")
    with pytest.raises(ValidationError):
        GetPerpTradesParams(pair="xau_usdt")
    assert prepare_params(PerpMarketFilter()) == {}


async def test_futures_methods_warn_deprecated(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(json=[])

    async with LNMClient(_auth_config()) as client:
        with pytest.warns(
            DeprecationWarning, match=r"client\.perp\.isolated\.get_running_trades\(\)"
        ):
            await client.futures.isolated.get_running_trades()


def test_nested_whole_floats_serialize_as_ints() -> None:
    # The server signs `JSON.stringify(body)`, which writes 64000.0 as 64000.
    params = PerpUpdateStoplossParams(
        id=TRADE_ID, **GOLD, stoploss=PerpStoploss(value=64_000)
    )
    body = prepare_params(params)
    assert body is not None
    assert json.dumps(body["stoploss"]) == '{"mode": "fixed", "value": 64000}'
