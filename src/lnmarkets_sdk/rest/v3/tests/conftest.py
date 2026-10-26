from collections.abc import Generator

import pytest

from lnmarkets_sdk.rest.v3._internal.models import APIException


def _skip_on_tier_limit() -> Generator[None, object, object]:
    """Turn a TIER_LIMIT_EXCEEDED API error into a skip.

    Signet enforces KYC tier limits on deposits and trades (rolling 30-day
    caps per verification level). When the test account hits one, that is an
    account state, not an SDK regression.
    """
    try:
        return (yield)
    except APIException as e:
        if e.error is not None and e.error.code == "TIER_LIMIT_EXCEEDED":
            pytest.skip(f"signet account tier limit reached: {e.error.message}")
        raise


@pytest.hookimpl(wrapper=True)
def pytest_runtest_setup(item: pytest.Item) -> Generator[None, object, object]:
    return (yield from _skip_on_tier_limit())


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None, object, object]:
    return (yield from _skip_on_tier_limit())
