from django.db.models import Q
from django.views import generic

from party.models import Party


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
        query = self.request.GET.get("search", None)
        if query:
            ctx["results"] = Party.objects.filter(
                Q(name__icontains=query) | Q(trips__display_name__icontains=query)
            ).order_by("date_start").distinct()
        return ctx
