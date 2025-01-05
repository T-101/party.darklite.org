import sys
import sqlite3
import rest_framework

from django import VERSION as DJANGO_VERSION
from django.contrib import messages
from django.db.models import Q, Count, F, When, Value, Case
from django.db.models.functions import Lower
from django.shortcuts import redirect
from django.views import generic
from django_countries import countries

from party.models import Party, Trip
from common.parsers import get_dependency_version


class LandingPageView(generic.TemplateView):
    template_name = 'party/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['upcoming_parties'] = (Party.upcoming_parties
                                   .filter(visible=True)
                                   .annotate(towards_party_count=Count("trips",
                                                                       filter=Q(trips__towards_party=True)),
                                             towards_home_count=Count("trips",
                                                                      filter=Q(trips__towards_party=False))
                                             )
                                   )
        ctx['past_parties'] = Party.past_parties.filter(visible=True)
        return ctx


class AboutView(generic.TemplateView):
    template_name = 'party/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["django_version"] = '.'.join(map(str, list(DJANGO_VERSION[0:3])))
        ctx["rest_framework_version"] = rest_framework.VERSION
        ctx["python_version"] = sys.version.split(" ")[0]
        ctx["sqlite_version"] = sqlite3.version
        ctx["bootstrap_version"] = get_dependency_version("bootstrap")
        ctx["fontawesome_version"] = get_dependency_version("font-awesome")
        ctx["jquery_version"] = get_dependency_version("jquery")
        return ctx


class SearchView(generic.TemplateView):
    template_name = 'party/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("search", None)

        if query and self.request.user.is_authenticated:
            filters = Q()
            for item in query.split():
                item = item.strip()
                if item.isdigit() and int(item) >= 2012:
                    filters &= Q(date_start__year=item)
                else:
                    filters &= (
                            Q(name__icontains=item) |
                            Q(trips__display_name__icontains=item) |
                            Q(country__icontains=item) |
                            Q(location__icontains=item)
                    )

            ctx["results"] = (Party.objects.filter(filters).order_by("date_start__year", Lower("name")).distinct())
        ctx["query"] = query
        return ctx


class StatsView(generic.TemplateView):
    template_name = 'party/stats.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, level=messages.WARNING, message="You need to be logged in to view stats")
            return redirect("party:landing_page")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        whens = [When(country_code=k, then=Value(v)) for k, v in dict(countries).items()]
        ctx["parties"] = Party.objects \
                             .filter(trips__towards_party=True, visible=True) \
                             .distinct() \
                             .annotate(Count("trips")) \
                             .order_by("-trips__count")[:10]
        ctx["display_names"] = Trip.objects \
                                   .filter(towards_party=True) \
                                   .values("display_name") \
                                   .annotate(count=Count("display_name")) \
                                   .order_by("-count")[:10]
        ctx["countries"] = list(Party.objects.filter(visible=True).exclude(country__name="None")
                                .annotate(country_code=F("country"))
                                .annotate(country_name=Case(*whens))
                                .values("country_code", "country_name")
                                .annotate(count=Count(F("country_code")))
                                .order_by("-count"))

        ctx["countries_piechart"] = [
            [x.get("country_name") for x in ctx["countries"]],
            [x.get("count") for x in ctx["countries"]]
        ]

        ctx["transportation"] = list(Trip.objects
                                     .values("type")
                                     .annotate(count=Count("type"))
                                     .order_by("-count"))

        ctx["transportation_piechart"] = [
            [x.get("type").capitalize() for x in ctx["transportation"]],
            [x.get("count") for x in ctx["transportation"]]
        ]

        ctx["towns"] = Trip.objects \
                           .filter(towards_party=True) \
                           .values("departure_town") \
                           .annotate(count=Count("departure_town")) \
                           .order_by("-count")[:10]
        ctx["airlines"] = Trip.objects \
                              .filter(type=Trip.PLANE, detail1__iregex=r"\S\S.+") \
                              .values("detail1") \
                              .annotate(count=(Count(Lower("detail1")))) \
                              .order_by("-count")[:10]
        ctx["trips_per_year"] = Trip.objects \
                                    .filter(towards_party=True) \
                                    .values("departure_datetime__year") \
                                    .annotate(count=Count("departure_datetime__year")) \
                                    .order_by("-count")[:10]
        ctx["trips_per_country"] = Trip.objects \
                                       .filter(towards_party=True) \
                                       .values("departure_country") \
                                       .annotate(count=Count("departure_country")) \
                                       .order_by("-count")[:10]
        return ctx
