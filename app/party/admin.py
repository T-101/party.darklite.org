import os
import re
import json

from django.contrib import admin
from django.conf import settings
from django.utils.dateparse import parse_datetime

from django_object_actions import DjangoObjectActions

from party.models import Party, Trip


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date_start',
        'date_end',
        'location',
        'country',
        'www',
        'slug',
        'created_dt',
        'created_by',
    )
    list_filter = ('date_start', 'date_end', 'created_dt', 'created_by')
    search_fields = ('name', 'slug', 'created_by__email')
    prepopulated_fields = {'slug': ['name']}
    list_select_related = ["created_by"]


@admin.register(Trip)
class TripAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        'id', 'party', 'display_name', 'type',
        'departure_town', 'departure_country', 'departure_datetime',
        'arrival_town', 'arrival_country', 'arrival_datetime',
        'detail1', 'detail2',
        'towards_home',
        'created_by',
    )
    search_fields = ['party__name', 'display_name', 'departure_town', 'arrival_town',
                     'detail1', 'detail2', 'created_by__email', 'created_by__display_name']
    list_filter = ('departure_datetime', 'arrival_datetime', 'towards_home')
    autocomplete_fields = ['party']

    def import_trips(self, request, obj):
        file_name = os.path.join(settings.BASE_DIR, "tdump.json")
        with open(file_name, "r") as raw_data:
            data = json.loads(raw_data.read())
        ret_arr = []
        regex = re.compile(r"(?:^([a-z]{2})$|^.* ([a-z]{2}$))", re.IGNORECASE)
        for item in data:
            print(item)
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
            trip.party = Party.objects.get(name__exact=item.get("party").get("name"), date_start__year=item.get("party").get("start_year"))
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
            trip.towards_home = item.get("towards_home")
            ret_arr.append(trip)
        Trip.objects.bulk_create(ret_arr)

    def import_flights(self, request, obj):
        file_name = os.path.join(settings.BASE_DIR, "fdump.json")
        with open(file_name, "r") as raw_data:
            data = json.loads(raw_data.read())
        ret_arr = []
        for item in data:
            print(item)
            trip = Trip()
            trip.display_name = item.get("display_name")
            trip.departure_town = item.get("departure_town")
            trip.departure_country = item.get("departure_country")
            trip.departure_datetime = parse_datetime(item.get("departure_datetime"))
            trip.party = Party.objects.get(name__exact=item.get("party").get("name"), date_start__year=item.get("party").get("start_year"))
            trip.arrival_town = item.get("arrival_town")
            trip.arrival_country = item.get("arrival_country")
            trip.arrival_datetime = parse_datetime(item.get("arrival_datetime"))
            trip.type = item.get("type")
            trip.detail1 = item.get("detail1")
            trip.detail2 = item.get("detail2")
            trip.towards_home = item.get("towards_home")
            ret_arr.append(trip)
        Trip.objects.bulk_create(ret_arr)

    changelist_actions = ["import_trips", "import_flights"]
