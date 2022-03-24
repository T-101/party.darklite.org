from dal import autocomplete
from django.db.models import Q
from django.db.models.functions import Lower
from django_countries import countries

from authentication.models import User
from common.mixins import AuthenticatedOr403Mixin, SuperUserOr403Mixin


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


class UserAutoComplete(SuperUserOr403Mixin, autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = User.objects.order_by(Lower("display_name"))

        if self.q:
            qs = qs.filter(display_name__istartswith=self.q)

        return qs
