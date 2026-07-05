import logging
from typing import Any, TypedDict


logger = logging.getLogger(__name__)


class RequestLogEntry(TypedDict):
    method: str
    path: str
    status_code: int


class RequestLoggingMiddleware:
    """Middleware that logs incoming requests and outgoing responses."""

    def __init__(self, get_response: Any) -> None:
        """
        Store the next callable in the middleware chain.

        Args:
            get_response: The next middleware or view callable.
        """
        self.get_response = get_response

    def __call__(self, request: Any) -> Any:
        """Log request start and end around the view execution.

        Args:
            request: The Django HTTP request object.

        Returns:
            The Django HTTP response object returned by the view or later middleware.

        Raises:
            Any exception raised by the view or later middleware is propagated.
        """
        request_log: RequestLogEntry = {
            'method': request.method,
            'path': request.get_full_path(),
            'status_code': 0,
        }

        logger.info('Request started: %s %s', request_log['method'], request_log['path'])
        response = self.get_response(request)

        request_log['status_code'] = response.status_code
        logger.info(
            'Request finished: %s %s -> %s',
            request_log['method'],
            request_log['path'],
            request_log['status_code'],
        )
        return response
