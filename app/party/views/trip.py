from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import generic

from party.forms import TripForm, TripFormNative
from party.models import Party, Trip


class TripCreateView(generic.CreateView):
    template_name = 'party/trip_create.html'
    model = Trip

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['is_required'] = True
        return kwargs

    def form_valid(self, form):
        form.instance.display_name = self.request.user.display_name
        form.instance.party = Party.objects.get(slug=self.kwargs.get("slug"))
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user_agent.is_mobile:
            return TripFormNative
        return TripForm

    def get_success_url(self):
        return reverse("party:detail", args=[self.kwargs.get("slug")])


class JourneyCreateView(generic.CreateView):
    template_name = 'party/journey_create.html'
    form_class = TripForm
    model = Trip

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["party"] = Party.objects.get(slug=self.kwargs.get("slug"))
        if self.request.user_agent.is_mobile:
            ctx["inbound"] = TripFormNative(prefix="inbound", initial={"towards_home": "False"})
            ctx["outbound"] = TripFormNative(prefix="outbound", initial={"towards_home": "True"})
        else:
            ctx["inbound"] = TripForm(prefix="inbound", initial={"towards_home": "False"})
            ctx["outbound"] = TripForm(prefix="outbound", initial={"towards_home": "True"})

        return ctx

    def form_valid(self, form):
        initial = {
            "created_by": self.request.user,
            "type": Trip.PLANE,
            "handle": "WWW PIER WWW",
            "party": Party.objects.get(slug=self.kwargs.get("slug"))
        }
        inbound_form = TripForm(self.request.POST, prefix="inbound", is_required=True)
        outbound_form = TripForm(self.request.POST, prefix="outbound", is_required=True,
                                 initial={"towards_home": "True"})
        errors = []

        if inbound_form.changed_data and inbound_form.is_valid():
            for item in initial:
                setattr(inbound_form.instance, item, initial.get(item))
            inbound_form.save()
        if inbound_form.changed_data and not inbound_form.is_valid():
            errors.append("inbound")
        if outbound_form.changed_data and outbound_form.is_valid():
            for item in initial:
                setattr(outbound_form.instance, item, initial.get(item))
            outbound_form.save()
        if outbound_form.changed_data and not outbound_form.is_valid():
            errors.append("outbound")
        if errors:
            print("ERRORS FOUND", inbound_form.errors)
            print("FORM CLEANED DATA", inbound_form.cleaned_data)
            print("FORM INSTANCE", inbound_form.instance.departure_country)
            return render(self.request, self.template_name, {
                'party': Party.objects.get(slug=self.kwargs.get("slug")),
                'inbound': TripForm(self.request.POST, prefix="inbound",
                                    is_required="inbound" in errors),
                'outbound': TripForm(self.request.POST, prefix="outbound",
                                     is_required="outbound" in errors)
            })
        return redirect("party:detail", self.kwargs.get("slug"))


class TripUpdateView(generic.UpdateView):
    template_name = 'party/trip_update.html'
    form_class = TripForm
    model = Trip

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user == self.get_object().created_by or self.request.user.is_superuser:
            return form
        raise Http404

    def get_success_url(self):
        return reverse("party:detail", args=[self.kwargs.get("slug")])
