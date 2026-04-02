from django.urls import path, include

from transparence.views.legal_case import LegalCaseViewSet
from transparence.views.party import PartyViewSet
from transparence.views.auth import AuthViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('', AuthViewSet, basename='token')
router.register('parties', PartyViewSet, basename='party')
router.register('legal-cases', LegalCaseViewSet, basename='legal_case')

urlpatterns = [ path('', include(router.urls)),]