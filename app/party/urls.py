from django.urls import path

from party.views.site import LandingPageView, AboutView, SearchView, StatsView, ShareView, health_check
from party.views.party import PartyListView, PartyCreateView, PartyDetailView, PartyUpdateView, DemopartyNetCreateView
from party.views.trip import TripToCreateView, TripFromCreateView, TripToUpdateView, TripFromUpdateView, \
    TripToCloneView, TripFromCloneView, TripDeleteView

app_name = "party"

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing_page"),
    path('about/', AboutView.as_view(), name="about"),
    path('search/', SearchView.as_view(), name="search"),
    path('stats/', StatsView.as_view(), name="stats"),
    path('health-check/', health_check, name="health-check"),
    path('shared/<str:short_uuid>/', ShareView.as_view(), name="shared"),
    path('list/', PartyListView.as_view(), name="list"),
    path('list/<int:year>/', PartyListView.as_view(), name="list-by-year"),
    path('list/<str:country>/', PartyListView.as_view(), name="list-by-country"),
    path('list/<str:country>/<int:year>/', PartyListView.as_view(), name="list-by-country-and-year"),
    path('create/', PartyCreateView.as_view(), name="create"),
    path('create/demopartynet/', DemopartyNetCreateView.as_view(), name="demopartynet-create"),
    path('<slug:slug>/update/', PartyUpdateView.as_view(), name="update"),
    path('create-trip-to/<slug:slug>/', TripToCreateView.as_view(), name="create-trip-to"),
    path('create-trip-from/<slug:slug>/', TripFromCreateView.as_view(), name="create-trip-from"),
    path('clone-trip-to/<slug:slug>/from_trip/<int:trip>/', TripToCloneView.as_view(), name="clone-trip-to"),
    path('clone-trip-from/<slug:slug>/from_trip/<int:trip>/', TripFromCloneView.as_view(), name="clone-trip-from"),
    path('update-trip-to/<slug:slug>/<int:trip>/', TripToUpdateView.as_view(), name="update-trip-to"),
    path('update-trip-from/<slug:slug>/<int:trip>/', TripFromUpdateView.as_view(), name="update-trip-from"),
    path('<slug:slug>/delete-trip/<int:pk>/', TripDeleteView.as_view(), name="delete-trip"),
    path('<slug:slug>/', PartyDetailView.as_view(), name="detail")
]
