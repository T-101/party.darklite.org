from django.db.models import Q, Count, F
from django.views import generic

from party.models import Party, Trip


class LandingPageView(generic.TemplateView):
    template_name = 'party/landing_page.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['upcoming_parties'] = Party.upcoming_parties.all()
        ctx['past_parties'] = Party.past_parties.all()
        return ctx


class AboutView(generic.TemplateView):
    template_name = 'party/about.html'


class SearchView(generic.TemplateView):
    template_name = 'party/search.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("search", None)
        if query:
            ctx["results"] = Party.objects.filter(
                Q(name__icontains=query) | Q(trips__display_name__icontains=query)
            ).order_by("date_start").distinct()
        return ctx


class StatsView(generic.TemplateView):
    template_name = 'party/stats.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["parties"] = Party.objects \
                             .filter(trips__towards_party=True) \
                             .distinct() \
                             .annotate(Count("trips")) \
                             .order_by("-trips__count")[:10]
        ctx["display_names"] = Trip.objects \
                                   .filter(towards_party=True) \
                                   .values("display_name") \
                                   .annotate(count=Count("display_name")) \
                                   .order_by("-count")[:10]
        ctx["countries"] = Party.objects \
                               .annotate(country_code=F("country")) \
                               .values("country_code") \
                               .annotate(count=Count(F("country_code"))) \
                               .order_by("-count")[:10]

        return ctx
