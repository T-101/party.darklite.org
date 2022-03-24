from django.urls import path

from autocomplete_contrib.views import CountryAutoComplete, UserAutoComplete

urlpatterns = [
    path('dal-countries/', CountryAutoComplete.as_view(), name='dal-countries'),
    path('dal-users/', UserAutoComplete.as_view(), name='dal-users')
]
