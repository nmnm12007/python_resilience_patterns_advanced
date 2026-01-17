"""
Implements mapping of exceptions to Failure Object with Failure_Type
"""
import socket
import requests
from resilience_patterns_observability.policies.failure_type import (
    FailureType, Failure)

class FailureTranslator:
    @staticmethod
    def translate(exc:Exception) -> Failure:
        if isinstance(exc, (TimeoutError, socket.timeout, requests.Timeout)):
            return Failure(
                failure_type=FailureType.TIMEOUT,
                message=f"Timeout on {exc.__class__.__name__}",
                retryable=True,
                original_exception=exc
            )

        if isinstance(exc, (ConnectionError, requests.ConnectionError)):
            return Failure(
                failure_type=FailureType.CONNECTION,
                message=f"Connection error on {exc.__class__.__name__}",
                retryable=True,
                original_exception=exc

            )

        if isinstance(exc, requests.HTTPError) and exc.response is not None:
            if exc.response.status_code == 429:
                return Failure(
                    failure_type=FailureType.VALIDATION,
                    message= str(exc),
                    retryable=False,
                    original_exception=exc
                )

        return Failure(
            failure_type=FailureType.UNKNOWN,
            message=str(exc),
            retryable=False,
            original_exception=exc
        )