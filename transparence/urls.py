from django.urls import path, include

from transparence.views.party import PartyViewSet
from transparence.views.auth import AuthViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('', AuthViewSet, basename='token')
router.register('parties', PartyViewSet, basename='party')

urlpatterns = [ path('', include(router.urls)),]