import feedparser
from datetime import datetime
import string

import requests
from django.db.models.functions import Lower
from django.contrib import messages
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ret_arr = []
        for i in ["country", "year"]:
            if self.kwargs.get(i):
                ret_arr.append(string.capwords(str(self.kwargs.get(i))))
        ctx["breadcrumb"] = ret_arr
        return ctx

    def get_queryset(self):
        qs = Party.objects.filter(visible=True).order_by(Lower("name"), "date_start")
        if "year" in self.kwargs:
            qs = qs.filter(date_start__year=self.kwargs.get("year"))
        if "country" in self.kwargs:
            qs = qs.filter(country__icontains=self.kwargs.get("country"))
        return qs


class PartyCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'party/party_create.html'
    model = Party
    queryset = Party.objects.filter(visible=True)

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
        form.instance.visible = True
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
        form.instance.visible = self.get_object().visible
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("party:detail", kwargs=self.kwargs)


class PartyDetailView(generic.DetailView):
    template_name = 'party/party_detail.html'
    model = Party

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trips = self.object.trips.order_by(Lower("display_name"))
        ctx["inbound"] = trips.filter(towards_party=True)
        ctx["outbound"] = trips.filter(towards_party=False)
        return ctx


class DemopartyNetCreateView(LoginRequiredMixin, generic.RedirectView):
    def get(self, request, *args, **kwargs):
        demopartynet_slug = request.GET.get("slug", None)
        if not demopartynet_slug:
            return redirect("party:landing_page")
        try:
            feed = fetch_demopartynet_parties()
        except Exception:
            messages.warning(self.request, "Error connecting to demoparty.net")
            return redirect("party:landing_page")
        if Party.objects.filter(slug=slugify(demopartynet_slug)):
            messages.info(request, "Party already exists")
            return redirect("party:detail", slug=slugify(demopartynet_slug))
        party_feed = [p for p in feed.entries if slugify(p.title) == slugify(demopartynet_slug)]
        if not party_feed:
            messages.warning(request, "Unknown party slug, unable to add party")
            return redirect("party:landing_page")
        if len(party_feed) != 1:
            messages.warning(self.request, "More than one party found with slug, unable to add party")
            return redirect("party:landing_page")
        party_feed = party_feed[0]
        address = []
        if party_feed.link:
            url = f"{party_feed.link}.jsonld"
            res = requests.get(url=url)
            if res.status_code == 200:
                j = res.json()
                if type(j.get("location")) == dict:
                    address.append(j.get("location", {}).get("address", {}).get("streetAddress", ""))
                    address.append(j.get("location", {}).get("address", {}).get("postalCode", ""))
                    address.append(j.get("location", {}).get("address", {}).get("addressLocality", ""))
        if len(address):
            address = [p for p in address if p != ""]
            address = ", ".join(address)
        else:
            address = "Unknown"
        defaults = {
            "name": party_feed.title,
            "www": party_feed.demopartynet_url,
            "date_start": datetime.strptime(party_feed.demopartynet_startdate, '%a, %d %b %Y %X %z'),
            "date_end": datetime.strptime(party_feed.demopartynet_enddate, '%a, %d %b %Y %X %z'),
            "location": address,
            "country": str(party_feed.demopartynet_country).upper(),
            "created_by": request.user
        }
        party, created = Party.objects.update_or_create(slug=slugify(demopartynet_slug), defaults=defaults)
        if created:
            messages.success(request, "Party created succesfully")
        return redirect('party:detail', party.slug)
