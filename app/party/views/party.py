import feedparser
from datetime import datetime

from django.db.models.functions import Lower
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.conf import settings

from common.mixins import LoginRequiredMixin
from party.forms import PartyForm, PartyFormNative
from party.models import Party


def fetch_demopartynet_parties():
    return feedparser.parse(settings.DEMOPARTYNET_RSS_FEED)


class PartyListView(generic.ListView):
    template_name = 'party/party_list.html'
    model = Party

    def get_queryset(self):
        qs = Party.objects.order_by(Lower("name"), "date_start")
        if "year" in self.kwargs:
            qs = qs.filter(date_start__year=self.kwargs.get("year"))
        return qs


class PartyCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'party/party_create.html'
    model = Party
    queryset = Party.objects.all()

    def get_form_class(self):
        if self.request.user_agent.is_mobile:
            return PartyFormNative
        return PartyForm

    @staticmethod
    def _get_demoparties():
        feed = fetch_demopartynet_parties()
        return [(p.title, p.link, p.demopartynet_country) for p in feed.entries]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["parties"] = self._get_demoparties()
        return ctx

    def get_success_url(self):
        return reverse("party:landing_page")


class PartyUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'party/party_create.html'
    model = Party
    form_class = PartyForm

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("party:detail", kwargs=self.kwargs)


class PartyDetailView(generic.DetailView):
    template_name = 'party/party_detail.html'
    model = Party

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trips = self.object.trips.select_related("created_by").order_by(Lower("display_name"))
        ctx["inbound"] = trips.filter(towards_party=True)
        ctx["outbound"] = trips.filter(towards_party=False)
        return ctx


class DemopartyNetCreateView(LoginRequiredMixin, generic.RedirectView):
    # https://www.demoparty.net/assembly/assembly-winter-2022.jsonld
    def get(self, request, *args, **kwargs):
        demopartynet_slug = request.GET.get("slug", None)
        if not demopartynet_slug:
            return redirect("party:landing_page")
        try:
            feed = fetch_demopartynet_parties()
        except Exception:
            messages.warning(request, "Error connecting to demoparty.net")
            return redirect("party:landing_page")
        party_feed = [p for p in feed.entries if slugify(p.title) == slugify(demopartynet_slug)]
        if not party_feed:
            return redirect("party:landing_page")
        if len(party_feed) != 1:
            return HttpResponse("Multiple party slug error. Contact someone")
        defaults = {
            "name": party_feed[0].title,
            "www": party_feed[0].demopartynet_url,
            "date_start": datetime.strptime(party_feed[0].demopartynet_startdate, '%a, %d %b %Y %X %z'),
            "date_end": datetime.strptime(party_feed[0].demopartynet_enddate, '%a, %d %b %Y %X %z'),
            "location": "Unknown",
            "country": str(party_feed[0].demopartynet_country).upper(),
            "created_by": request.user
        }
        party, _ = Party.objects.update_or_create(slug=slugify(demopartynet_slug), defaults=defaults)
        return redirect('party:detail', party.slug)
