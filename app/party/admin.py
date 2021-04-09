# -*- coding: utf-8 -*-
import csv

import requests
from django.contrib import admin
from django.core.files.base import ContentFile
from django_object_actions import DjangoObjectActions

from .models import Party, Airport, Trip


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


@admin.register(Airport)
class AirportAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('id', 'name', 'iata_code', 'country')
    search_fields = ('name',)

    def refetch_airports(self, request, queryset):
        res = requests.get('https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv')
        if res.status_code != 200:
            return
        res.encoding = 'utf-8'
        f = ContentFile(res.text)
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('name') and row.get('iso_country') and row.get('iata_code'):
                a, c = Airport.objects.get_or_create(iata_code=row.get('iata_code'))
                a.name = row.get('name')
                a.country = row.get('iso_country')
                a.save()

        self.message_user(request, "Airports refetched")

    changelist_actions = ('refetch_airports',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'party', 'handle', 'type',
        'departure_town', 'departure_country', 'departure_datetime',
        'arrival_town', 'arrival_country', 'arrival_datetime',
        'detail1', 'detail2',
        'towards_home',
        'created_by',
    )
    search_fields = ['party__name', 'handle', 'departure_town', 'arrival_town', 'detail1', 'detail2']
    list_filter = ('party', 'departure_datetime', 'arrival_datetime', 'towards_home', 'created_by',)
    autocomplete_fields = ['party']
