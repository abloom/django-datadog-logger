import traceback
import logging
from django.http.response import Http404


logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            log_entry_dict = {
                "error.kind": 404,
                "error.message": str(exception),
                "error.stack": traceback.format_exception(exception),
            }
            logger.warning(f"Http404: {exception}", extra=log_entry_dict)
        else:
            logger.exception(exception)

    def process_response(self, request, response):
        return response
