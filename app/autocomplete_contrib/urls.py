from django.urls import path

from autocomplete_contrib.views import CountryAutoComplete

urlpatterns = [
    path('dal-countries/', CountryAutoComplete.as_view(), name='dal-countries'),
]
