import time
import logging

logger = logging.getLogger("api_usage")


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        ip = request.META.get("REMOTE_ADDR")

        logger.info(
            {
                "path": request.path,
                "method": request.method,
                "status": response.status_code,
                "duration": round(duration, 3),
                "ip": ip,
            }
        )

        return response
