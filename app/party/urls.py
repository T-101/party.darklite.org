from django.urls import path

from party.views.site import LandingPageView, AboutView, SearchView
from party.views.party import PartyListView, PartyCreateView, PartyDetailView, PartyUpdateView, DemopartyNetCreateView
from party.views.trip import TripToCreateView, TripFromCreateView, TripToUpdateView, TripFromUpdateView, \
    TripToCloneView, TripFromCloneView

app_name = "party"

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing_page"),
    path('about/', AboutView.as_view(), name="about"),
    path('search/', SearchView.as_view(), name="search"),
    path('list/', PartyListView.as_view(), name="list"),
    path('list/<int:year>/', PartyListView.as_view(), name="list-by-year"),
    path('create/', PartyCreateView.as_view(), name="create"),
    path('create/demopartynet/', DemopartyNetCreateView.as_view(), name="demopartynet-create"),
    path('<slug:slug>/update/', PartyUpdateView.as_view(), name="update"),
    path('create-trip-to/<slug:slug>/', TripToCreateView.as_view(), name="create-trip-to"),
    path('create-trip-from/<slug:slug>/', TripFromCreateView.as_view(), name="create-trip-from"),
    path('clone-trip-to/<slug:slug>/from_trip/<int:trip>/', TripToCloneView.as_view(), name="clone-trip-to"),
    path('clone-trip-from/<slug:slug>/from_trip/<int:trip>/', TripFromCloneView.as_view(), name="clone-trip-from"),
    path('update-trip-to/<slug:slug>/<int:trip>/', TripToUpdateView.as_view(), name="update-trip-to"),
    path('update-trip-from/<slug:slug>/<int:trip>/', TripFromUpdateView.as_view(), name="update-trip-from"),
    path('<slug:slug>/', PartyDetailView.as_view(), name="detail")
]
