"""A retried request must wait, or the retry budget buys nothing.

Pair 0029's cell in matrix v7 died on a Cloudflare 504.  It had a budget of two
retries and it used both -- and the run record shows the three attempts issued
*nine microseconds* apart:

    attempt 1  finished 12:19:44.431970
    attempt 2  started  12:19:44.431979
    attempt 3  started  12:20:45.220335

All three landed inside the same 60-second gateway-timeout window, so the cell
spent three minutes of wall clock to fail exactly as it would have on a single
attempt, and the pair produced no result.  A budget without a delay is not a
retry policy; it is the same request three times.

The reference implementation in `utils/agent/runtime.py` already had the shape
this needed -- an explicit delay schedule plus an honoured `Retry-After` -- so
these tests pin that behaviour here.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.responder import (  # noqa: E402
    TRANSPORT_RETRY_DELAYS,
    _provider_retry_after_seconds,
    _retry_delay,
    _retryable_error,
)


class Plain(Exception):
    pass


class WithHeader(Exception):
    def __init__(self, seconds):
        super().__init__("rate limited")
        self.headers = {"retry-after": str(seconds)}


class WithBody(Exception):
    def __init__(self, seconds):
        super().__init__("rate limited")
        self.body = {"retry_after": seconds}


class WithResponse(Exception):
    def __init__(self, seconds):
        super().__init__("rate limited")

        class R:
            headers = {"Retry-After": str(seconds)}

        self.response = R()


def test_the_schedule_grows_and_starts_above_a_gateway_timeout_retry():
    """The first wait has to be long enough to be a different request.

    Not necessarily longer than the timeout itself -- that would cost minutes on
    a transient blip -- but far enough from zero that the upstream has had a
    chance to change state.
    """

    delays = [_retry_delay(Plain(), i) for i in range(len(TRANSPORT_RETRY_DELAYS) + 2)]
    assert delays[0] >= 5.0, "the first retry must not be immediate"
    assert delays == sorted(delays), "the schedule must be non-decreasing"
    # Past the end of the schedule it saturates rather than growing without bound
    # or falling back to zero.
    assert delays[-1] == TRANSPORT_RETRY_DELAYS[-1]
    assert delays[-2] == TRANSPORT_RETRY_DELAYS[-1]


@pytest.mark.parametrize("factory", [WithHeader, WithBody, WithResponse])
def test_a_provider_hint_overrides_the_schedule(factory):
    """The provider knows when it will be ready; a schedule is only a fallback.

    Ignoring the hint on a 429 retries a rate limit into another rate limit.
    """

    assert _retry_delay(factory(37), 0) == 37.0
    # Even at a schedule position whose default is larger.
    assert _retry_delay(factory(3), 4) == 3.0


def test_a_hint_is_read_through_the_exception_chain():
    """Providers wrap; the hint is usually on the inner error."""

    outer = Plain()
    outer.__cause__ = WithHeader(11)
    assert _provider_retry_after_seconds(outer) == 11.0

    outer2 = Plain()
    outer2.__context__ = WithBody(13)
    assert _provider_retry_after_seconds(outer2) == 13.0


@pytest.mark.parametrize("value", ["0", "-5", "", "soon", None])
def test_a_useless_hint_falls_back_to_the_schedule(value):
    """A zero or unparseable `Retry-After` must not mean "retry immediately"."""

    exc = Plain()
    exc.headers = {"retry-after": value}
    assert _provider_retry_after_seconds(exc) is None
    assert _retry_delay(exc, 0) == TRANSPORT_RETRY_DELAYS[0]


def test_a_self_referential_exception_chain_terminates():
    """A cycle in `__cause__` must not hang the reader."""

    a, b = Plain(), Plain()
    a.__cause__ = b
    b.__cause__ = a
    start = time.perf_counter()
    assert _provider_retry_after_seconds(a) is None
    assert time.perf_counter() - start < 1.0


def test_the_gateway_timeout_that_killed_pair_0029_is_retryable():
    """Belt and braces: the classification was already right, keep it that way."""

    class Gateway(Exception):
        status_code = 504

    assert _retryable_error(Gateway()) is True


def test_a_schema_violation_is_not_retried():
    """Retrying a malformed structured output just spends the budget."""

    assert _retryable_error(ValueError("structured validation failed")) is False
    assert _retryable_error(TypeError("bad kwargs")) is False
