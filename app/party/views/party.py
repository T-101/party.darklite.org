import string

import requests
from django.db.models.functions import Lower
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views import generic

from common.mixins import LoginRequiredMixin
from party.forms import PartyForm, PartyFormNative
from party.models import Party


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

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.visible = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("party:landing_page")


class PartyUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'party/party_create.html'
    model = Party
    form_class = PartyForm

    def get(self, request, *args, **kwargs):
        party = self.get_object()
        if party.has_ended:
            messages.warning(request, "Cannot modify a party that has ended")
            return redirect(reverse("party:landing_page"))
        return super().get(request, *args, **kwargs)

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
        trips = self.object.trips.select_related("created_by").order_by(Lower("display_name"))
        ctx["inbound"] = trips.filter(towards_party=True)
        ctx["outbound"] = trips.filter(towards_party=False)
        return ctx


class DemopartyNetCreateView(LoginRequiredMixin, generic.RedirectView):
    def get(self, request, *args, **kwargs):
        demopartynet_id = request.GET.get("id", None)
        address = []
        defaults = {
            "created_by": request.user
        }

        url = f"https://www.demoparty.net/api/events/{demopartynet_id}"
        res = requests.get(url=url, timeout=10)
        if res.status_code != 200:
            messages.warning(request, "Error fetching data from demoparty.net")
            return redirect(reverse("party:landing_page"))

        j = res.json()
        if j.get("location", {}).get("@type") == "VirtualLocation":
            defaults["location"] = "Online"
        else:
            address.append(j.get("location", {}).get("address", {}).get("streetAddress", ""))
            address.append(j.get("location", {}).get("address", {}).get("postalCode", ""))
            address.append(j.get("location", {}).get("address", {}).get("addressLocality", ""))
            defaults["location"] = ", ".join([p for p in address if p != ""])
        defaults["name"] = j.get("name")
        defaults["www"] = j.get("url")
        try:
            defaults["date_start"] = timezone.datetime.strptime(j.get("startDate"), "%Y-%m-%dT%H:%M:%S%z").date()
            defaults["date_end"] = timezone.datetime.strptime(j.get("endDate"), "%Y-%m-%dT%H:%M:%S%z").date()
        except ValueError:
            messages.warning(request, "Error parsing dates from demoparty.net")
            return redirect(reverse("party:landing_page"))
        defaults["country"] = j.get("location", {}).get("address", {}).get("addressCountry", "")[-2:]

        party, _ = Party.objects.update_or_create(slug=slugify(defaults["name"]), defaults=defaults)
        return redirect('party:detail', party.slug)
