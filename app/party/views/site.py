import sys

from django import VERSION as DJANGO_VERSION
from django.db.models import Q, Count, F, When, Value, Case
from django.views import generic
from django_countries import countries

from party.models import Party, Trip


class LandingPageView(generic.TemplateView):
    template_name = 'party/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['upcoming_parties'] = Party.upcoming_parties.filter(visible=True)
        ctx['past_parties'] = Party.past_parties.filter(visible=True)
        return ctx


class AboutView(generic.TemplateView):
    template_name = 'party/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["django_version"] = '.'.join(map(str, list(DJANGO_VERSION[0:3])))
        ctx["python_version"] = sys.version.split(" ")[0]
        return ctx


class SearchView(generic.TemplateView):
    template_name = 'party/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("search", None)
        if query:
            ctx["results"] = Party.objects.filter(visible=True).filter(
                Q(name__icontains=query) | Q(trips__display_name__icontains=query)
            ).order_by("date_start").distinct()
        return ctx


class StatsView(generic.TemplateView):
    template_name = 'party/stats.html'

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
        ctx["countries"] = Party.objects.filter(visible=True) \
                               .annotate(country_code=F("country")) \
                               .annotate(country_name=Case(*whens)) \
                               .values("country_code", "country_name") \
                               .annotate(count=Count(F("country_code"))) \
                               .order_by("-count")[:10]

        return ctx
