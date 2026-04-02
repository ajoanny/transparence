from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet

from transparence.models import ApiClient
from transparence.models.refresh_token import RefreshToken


class AuthViewSet(ViewSet):

    @action(detail=False, methods=["post"])
    def token(self, request):
        client_id = request.data.get("client_id")
        client_secret = request.data.get("client_secret")

        if not client_id or not client_secret:
            return Response(
                {"error": "Missing credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        client = ApiClient.objects.filter(client_id=client_id).first()

        if client is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not client.authenticate(client_secret):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(client.token(), status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="token/refresh")
    def refresh(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Missing refresh_token"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = RefreshToken.objects.get(token=refresh_token).client

            if client is None:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = client.refresh()
        except AuthenticationFailed:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(token, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="token/revoke")
    def revoke(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Missing refresh_token"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            client = RefreshToken.objects.get(token=refresh_token).client

            if client is None:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            client.revoke()
        except RefreshToken.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(None, status=status.HTTP_204_NO_CONTENT)
