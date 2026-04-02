from datetime import datetime, timedelta, timezone
import uuid
import jwt
from django.db import models
import secrets
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed

from config import settings
from transparence.models.refresh_token import RefreshToken


class ApiClient(models.Model):
    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    jti = models.CharField(max_length=100, null=True, blank=True)


    def init(self):
        self.client_id = secrets.token_urlsafe(16)
        self.secret = secrets.token_urlsafe(24)
        self.hash_secret(self.secret)

    def hash_secret(self, secret):
        self.client_secret = make_password(secret)

    def authenticate(self, secret):
        return check_password(secret, self.client_secret)

    def token(self):
        now = datetime.now(timezone.utc)
        expired_at=now + timedelta(hours=1)

        refresh_token = secrets.token_urlsafe(64)
        RefreshToken.objects.filter(client=self).delete()
        RefreshToken.objects.create(client=self, token=refresh_token, expired_at=expired_at )
        self.jwt_revoked = False
        self.jti = str(uuid.uuid4())
        self.save()

        data = {
            "iss": "transparence_api",
            "sub": self.client_id,
            "exp": expired_at,
            "iat": now,
            "jti": self.jti,
        }
        access_token = jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def revoke(self):
        self.jti = None
        self.refresh_token.delete()
        self.save()

    def refresh(self):
        if not self.refresh_token.is_valid():
            raise AuthenticationFailed("Invalid refresh token")

        return self.token()

    def __str__(self):
      return self.name

    def check_secret(self, secret):
        return check_password(secret, self.client_secret)