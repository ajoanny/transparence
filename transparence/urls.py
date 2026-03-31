from django.urls import path
from transparence.views.party import list as party_list

urlpatterns = [
    path('parties/', party_list, name='party-list'),
]
