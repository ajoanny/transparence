from datetime import datetime, timezone
from django.db import models


class RefreshToken(models.Model):
    client = models.OneToOneField(
        "ApiClient", on_delete=models.CASCADE, related_name="refresh_token"
    )
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def is_valid(self):
        return self.expired_at >= datetime.now(timezone.utc)
