from django.template.defaultfilters import upper
from rest_framework.throttling import SimpleRateThrottle


class APIRateLimiting(SimpleRateThrottle):
    scope = "api_key"

    def get_cache_key(self, request, view):
        auth = request.headers.get("Authorization", "")
        [type, key] = auth.split(" ")
        if upper(type) == "API-KEY":
            return key

        return None
