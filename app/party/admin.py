from django.contrib import admin

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
