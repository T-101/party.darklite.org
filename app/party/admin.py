import os
import re
import json

from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from django_countries import countries
from django_object_actions import DjangoObjectActions

from party.models import Party, Trip


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date_start',
        'visible',
        'location',
        'country_name',
        'www',
        'slug',
        'created_dt',
        'created_by',
    )

    def country_name(self, obj):
        return obj.country.name

    country_name.admin_order_field = 'country'

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term,
        )
        queryset |= self.model.objects.filter(country__icontains=search_term)
        return queryset, may_have_duplicates

    list_filter = ('visible', 'date_start', 'date_end', 'created_dt')
    search_fields = ('name', 'created_by__email')
    readonly_fields = ["slug"]
    list_select_related = ["created_by"]


@admin.register(Trip)
class TripAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        'id', 'party', 'display_name', 'type',
        'departure_town',
        'departure_country_name',
        'departure_datetime',
        'arrival_town',
        'arrival_country_name',
        'arrival_datetime',
        'detail1', 'detail2',
        'towards_party',
        # 'created_by',
    )
    search_fields = ['party__name', 'display_name', 'departure_town', 'departure_country', 'arrival_town',
                     'arrival_country',
                     'detail1', 'detail2', 'created_by__email', 'created_by__display_name']
    list_filter = ('departure_datetime', 'arrival_datetime', 'towards_party', "type")
    autocomplete_fields = ['party', 'created_by']
    date_hierarchy = "departure_datetime"
    list_select_related = ["party", "created_by"]

    def departure_country_name(self, obj):
        return obj.departure_country.name

    departure_country_name.admin_order_field = 'departure_country'

    def arrival_country_name(self, obj):
        return obj.arrival_country.name

    arrival_country_name.admin_order_field = 'arrival_country'

    def import_trips(self, request, obj):
        file_name = os.path.join(settings.BASE_DIR, "tdump.json")
        with open(file_name, "r") as raw_data:
            data = json.loads(raw_data.read())
        ret_arr = []
        regex = re.compile(r"(?:^([a-z]{2})$|^.* ([a-z]{2}$))", re.IGNORECASE)
        for item in data:
            trip = Trip()
            trip.display_name = item.get("display_name")
            trip.departure_town = item.get("departure_town")
            r = regex.search(trip.departure_town)
            if r:
                if r.group(1) is None:
                    index = 2
                else:
                    index = 1
                trip.departure_country = r.group(index).upper()
            else:
                trip.departure_country = item.get("departure_country")
            trip.departure_datetime = parse_datetime(item.get("departure_datetime"))
            trip.party = Party.objects.get(name__exact=item.get("party").get("name"),
                                           date_start__year=item.get("party").get("start_year"))
            trip.arrival_town = item.get("arrival_town")
            r = regex.search(trip.arrival_town)
            if r:
                if r.group(1) is None:
                    index = 2
                else:
                    index = 1
                trip.arrival_country = r.group(index).upper()
            else:
                trip.arrival_country = item.get("arrival_country")
            trip.arrival_datetime = parse_datetime(item.get("arrival_datetime"))
            trip.type = item.get("type")
            trip.detail1 = item.get("detail1")
            trip.detail2 = item.get("detail2")
            trip.towards_party = item.get("towards_party")
            ret_arr.append(trip)
        Trip.objects.bulk_create(ret_arr)

    def import_flights(self, request, obj):
        file_name = os.path.join(settings.BASE_DIR, "fdump.json")
        with open(file_name, "r") as raw_data:
            data = json.loads(raw_data.read())
        ret_arr = []
        for item in data:
            trip = Trip()
            trip.display_name = item.get("display_name")
            trip.departure_town = item.get("departure_town")
            trip.departure_country = item.get("departure_country")
            trip.departure_datetime = parse_datetime(item.get("departure_datetime"))
            trip.party = Party.objects.get(name__exact=item.get("party").get("name"),
                                           date_start__year=item.get("party").get("start_year"))
            trip.arrival_town = item.get("arrival_town")
            trip.arrival_country = item.get("arrival_country")
            trip.arrival_datetime = parse_datetime(item.get("arrival_datetime"))
            trip.type = item.get("type")
            trip.detail1 = item.get("detail1")
            trip.detail2 = item.get("detail2")
            trip.towards_party = item.get("towards_party")
            ret_arr.append(trip)
        Trip.objects.bulk_create(ret_arr)

    changelist_actions = ["import_trips", "import_flights"]

    def update_country(self, request, queryset):
        if 'apply' in request.POST:
            queryset.update(**{f"{request.POST.get('direction')}_country": request.POST.get("country")})
            self.message_user(request, "Changed status on {} trips".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())
        return render(request, 'admin/update_country.html',
                      context={"queryset": queryset, "country_list": list(countries)})

    def update_trip_type(self, request, queryset):
        if 'apply' in request.POST:
            queryset.update(type=request.POST.get("trip_type"))
            self.message_user(request, "Changed status on {} trips".format(queryset.count()))
            return HttpResponseRedirect(request.get_full_path())
        return render(request, 'admin/update_trip_type.html',
                      context={"queryset": queryset, "trip_type_list": Trip.TYPES})

    def set_toward_party_true(self, request, queryset):
        queryset.update(towards_party=True)
        return HttpResponseRedirect(request.get_full_path())

    def set_toward_party_false(self, request, queryset):
        queryset.update(towards_party=False)
        return HttpResponseRedirect(request.get_full_path())

    def update_trip_created_by(self, request, queryset):
        if 'apply' in request.POST:
            created_by = get_user_model().objects.get(pk=request.POST.get('created_by'))
            queryset.update(created_by=created_by)
            self.message_user(request, f"Trips set to {created_by}")
            return HttpResponseRedirect(request.get_full_path())
        user_list = get_user_model().objects.order_by(Lower("display_name")).values_list("id", "display_name")
        return render(request, 'admin/update_trip_create_by.html',
                      context={"queryset": queryset,
                               "created_by_list": user_list})

    actions = ['update_country', 'update_trip_type', 'set_toward_party_true', 'set_toward_party_false',
               'update_trip_created_by']
