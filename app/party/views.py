import feedparser
from datetime import datetime

from django.db.models.functions import Lower
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.conf import settings

from party.forms import PartyForm, TripForm, TripFormNative
from party.models import Party, Trip


def fetch_demopartynet_parties():
    return feedparser.parse(settings.DEMOPARTYNET_RSS_FEED)


class LandingPageView(generic.TemplateView):
    template_name = 'party/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['upcoming_parties'] = Party.upcoming_parties.all()
        ctx['past_parties'] = Party.past_parties.all()
        return ctx


class AboutView(generic.TemplateView):
    template_name = 'party/base.html'


class SearchView(generic.TemplateView):
    template_name = 'party/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["results"] = Party.objects.filter(name__icontains=self.request.GET.get("search", None)).order_by("date_start")
        return ctx


class PartyListView(generic.ListView):
    template_name = 'party/list.html'
    model = Party
    queryset = Party.objects.all()


class PartyCreateView(generic.CreateView):
    template_name = 'party/create.html'
    form_class = PartyForm
    model = Party
    queryset = Party.objects.all()

    @staticmethod
    def _get_demoparties():
        feed = fetch_demopartynet_parties()
        return [(p.title, p.link) for p in feed.entries]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["parties"] = self._get_demoparties()
        return ctx

    def get_success_url(self):
        return reverse("party:landing_page")


class PartyDetailView(generic.DetailView):
    template_name = 'party/detail.html'
    model = Party

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trips = self.object.trips.select_related("created_by").order_by(Lower("display_name"))
        ctx["inbound"] = trips.filter(towards_home=False)
        ctx["outbound"] = trips.filter(towards_home=True)
        return ctx


class PartyUpdateView(generic.UpdateView):
    template_name = 'party/create.html'
    model = Party
    form_class = PartyForm

    def get_success_url(self):
        return reverse("party:landing_page")


class DemopartyNetCreateView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        demopartynet_slug = request.GET.get("slug", None)
        if not demopartynet_slug:
            return redirect("party:landing_page")
        # TODO make a check for when connection fails
        # Now a connection error will end up in HTTP 500
        feed = fetch_demopartynet_parties()
        party_feed = [p for p in feed.entries if slugify(p.title) == slugify(demopartynet_slug)]
        if not party_feed:
            return redirect("party:landing_page")
        if len(party_feed) != 1:
            return HttpResponse("Multiple party slug error. Contact someone")
        Party.objects.update_or_create(slug=slugify(demopartynet_slug),
                                       defaults={
                                           "name": party_feed[0].title,
                                           "www": party_feed[0].demopartynet_url,
                                           "date_start": datetime.strptime(party_feed[0].demopartynet_startdate,
                                                                           '%a, %d %b %Y %X %z'),
                                           "date_end": datetime.strptime(party_feed[0].demopartynet_enddate,
                                                                         '%a, %d %b %Y %X %z'),
                                           "location": "Unknown",
                                           "country": str(party_feed[0].demopartynet_country).upper()
                                       }
                                       )
        return HttpResponse(party_feed[0])
        return HttpResponse(demopartynet_slug)


class TripCreateView(generic.CreateView):
    template_name = 'party/create_flight.html'
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
    template_name = 'party/update_flight.html'
    form_class = TripForm
    model = Trip

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user == self.get_object().created_by or self.request.user.is_superuser:
            return form
        raise Http404

    def get_success_url(self):
        return reverse("party:detail", args=[self.kwargs.get("slug")])
