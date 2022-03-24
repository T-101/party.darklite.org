from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.views import generic
from party.forms import TripForm, TripFormNative
from party.models import Party, Trip


class FormModelMixin:
    model = Trip

    def get_form_class(self):
        if self.request.user_agent.is_mobile:
            return TripFormNative
        return TripForm

    def get_success_url(self):
        return reverse("party:detail", args=[self.kwargs.get("slug")])


class PartyMixin:
    def dispatch(self, request, *args, **kwargs):
        self.party = get_object_or_404(Party, slug=self.kwargs.get("slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['party'] = self.party
        ctx['towards_party'] = self.towards_party
        return ctx


class TripToCreateView(PartyMixin, FormModelMixin, generic.CreateView):
    template_name = 'party/trip_create_to.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = True
        self.party = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["display_name"] = self.request.user.display_name
        kwargs["is_required"] = True
        return kwargs

    def form_valid(self, form):
        form.instance.party = self.party
        form.instance.display_name = self.request.user.display_name
        form.instance.towards_party = self.towards_party
        return super().form_valid(form)


class TripFromCreateView(TripToCreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = False


class TripToUpdateView(FormModelMixin, PartyMixin, generic.UpdateView):
    template_name = 'party/trip_create_to.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = True
        self.party = None

    def get_object(self, queryset=None):
        trip = get_object_or_404(self.model, pk=self.kwargs.get("trip"))
        if not trip.created_by == self.request.user:
            raise PermissionDenied
        return trip

    def form_valid(self, form):
        form.instance.towards_party = self.towards_party
        return super().form_valid(form)


class TripFromUpdateView(TripToUpdateView):
    template_name = 'party/trip_create_to.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = False


class TripToCloneView(PartyMixin, FormModelMixin, generic.CreateView):
    template_name = 'party/trip_create_to.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = True
        self.party = None
        self.trip = None

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, pk=self.kwargs.get("trip"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["trip_instance"] = self.trip
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["display_name"] = self.request.user.display_name
        initial["departure_town"] = self.trip.departure_town
        initial["arrival_town"] = self.trip.departure_town
        initial["departure_datetime"] = self.trip.departure_datetime
        initial["arrival_datetime"] = self.trip.departure_datetime
        initial["type"] = self.trip.type
        initial["detail1"] = self.trip.detail1
        initial["detail2"] = self.trip.detail2
        return initial

    def form_valid(self, form):
        form.instance.towards_party = self.towards_party
        form.instance.party = self.party
        return super().form_valid(form)


class TripFromCloneView(TripToCloneView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.towards_party = False
        self.party = None
        self.trip = None
