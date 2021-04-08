from django.urls import path

from party.views import LandingPageView, AboutView, SearchView, PartyListView, PartyCreateView, PartyDetailView, \
    PartyUpdateView, FlightCreateView, FlightUpdateView, TravelCreateView, TravelUpdateView, DemopartyNetCreateView

app_name = "party"

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing_page"),
    path('about/', AboutView.as_view(), name="about"),
    path('search/', SearchView.as_view(), name="search"),
    path('list/', PartyListView.as_view(), name="list"),
    path('create/', PartyCreateView.as_view(), name="create"),
    path('create/demopartynet/', DemopartyNetCreateView.as_view(), name="demopartynet-create"),
    path('<slug:slug>/update/', PartyUpdateView.as_view(), name="update"),
    path('<slug:slug>/create-flight/', FlightCreateView.as_view(), name="create-flight"),
    path('<slug:slug>/create-flight/<int:pk>/', FlightCreateView.as_view(), name="create-flight"),
    path('<slug:slug>/update-flight/<int:pk>/', FlightUpdateView.as_view(), name="update-flight"),
    path('<slug:slug>/create-travel/', TravelCreateView.as_view(), name="create-travel"),
    path('<slug:slug>/create-travel/<int:pk>/', TravelCreateView.as_view(), name="create-travel"),
    path('<slug:slug>/update-travel/<int:pk>/', TravelUpdateView.as_view(), name="update-travel"),
    path('<slug:slug>/', PartyDetailView.as_view(), name="detail")
]
