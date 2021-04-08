from dal import autocomplete
from django.db.models import Q
from django.utils.html import format_html
from django_countries import countries
from django_countries.fields import Country

from common.mixins import AuthenticatedOr403Mixin
from party.models import Airport


class BaseAutoComplete(AuthenticatedOr403Mixin, autocomplete.Select2QuerySetView):
    search_fields = None
    expr = 'istartswith'

    def get_queryset(self):
        assert self.queryset is not None, 'Expected the `queryset` attribute to be specified.'
        assert self.search_fields is not None, 'Expected `fields_to_query` to contain at least one field.'
        qs = self.queryset
        if self.q:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{'%s__%s' % (field, self.expr): self.q})
            return qs.filter(q_objects)
        return qs


class CountryAutoComplete(AuthenticatedOr403Mixin, autocomplete.Select2ListView):

    def get_list(self):
        return countries


class Airports(AuthenticatedOr403Mixin, autocomplete.Select2QuerySetView):
    queryset = Airport.objects.all()

    def get_queryset(self):
        qs = self.queryset
        if self.q:
            iata = qs.filter(iata_code__istartswith=self.q)
            airport = qs.filter(name__icontains=self.q)
            return list(iata) + list(airport)
        return qs
