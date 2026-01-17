import time

from resilience_full_impl.cancellation.cancellation_token import CancellationToken
from resilience_full_impl.cancellation.exceptions import CancelledException


def test_deadline_cancellation():
    token = CancellationToken(deadline_seconds=1)

    time.sleep(1.5)

    try:
        token.throw_if_cancelled()
        print("❌ ERROR: cancellation not triggered")
    except CancelledException:
        print("✅ Deadline cancellation works")


def test_explicit_cancellation():
    token = CancellationToken()

    token.cancel()

    try:
        token.throw_if_cancelled()
        print("❌ ERROR: explicit cancellation not triggered")
    except CancelledException:
        print("✅ Explicit cancellation works")


if __name__ == "__main__":
    test_deadline_cancellation()
    test_explicit_cancellation()
