from django.urls import path

from party.views.site import LandingPageView, AboutView, SearchView
from party.views.party import PartyListView, PartyCreateView, PartyDetailView, PartyUpdateView, DemopartyNetCreateView
from party.views.trip import TripCreateView, TripUpdateView

app_name = "party"

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing_page"),
    path('about/', AboutView.as_view(), name="about"),
    path('search/', SearchView.as_view(), name="search"),
    path('list/', PartyListView.as_view(), name="list"),
    path('create/', PartyCreateView.as_view(), name="create"),
    path('create/demopartynet/', DemopartyNetCreateView.as_view(), name="demopartynet-create"),
    path('<slug:slug>/update/', PartyUpdateView.as_view(), name="update"),
    path('<slug:slug>/create-trip/', TripCreateView.as_view(), name="create-trip"),
    path('<slug:slug>/create-trip/<int:pk>/', TripCreateView.as_view(), name="create-trip"),
    path('<slug:slug>/update-trip/<int:pk>/', TripUpdateView.as_view(), name="update-trip"),
    path('<slug:slug>/', PartyDetailView.as_view(), name="detail")
]
