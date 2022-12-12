import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField
from django_extensions.db.fields import AutoSlugField

from common.parsers import strip_trailing_year
from party.managers import UpcomingPartyManager, PastPartyManager, PartyManager


class Party(models.Model):
    name = models.CharField(max_length=64)
    date_start = models.DateField()
    date_end = models.DateField()
    location = models.CharField(max_length=64)
    country = CountryField(multiple=False, null=True, blank=True)
    www = models.URLField(blank=True, null=True)
    slug = AutoSlugField(populate_from=["name", "date_start__year"])

    created_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Created datetime')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="created_parties")
    modified_dt = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Modified datetime')
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name="modified_parties")

    visible = models.BooleanField(default=True)

    objects = PartyManager()
    upcoming_parties = UpcomingPartyManager()
    past_parties = PastPartyManager()

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"

    def save(self, *args, **kwargs):
        if self.name.endswith(str(self.date_start.year)):
            self.name = strip_trailing_year(self.name)
        super().save(*args, **kwargs)

    @property
    def date_range(self):
        """
        Let's jump through some hoops to format a nice date range
        """
        if self.date_start == self.date_end:
            # One day parties
            return self.date_start.strftime('%b %e, %Y')

        date_start = self.date_start.strftime('%b %e %Y')
        date_end = self.date_end.strftime('%b %e %Y')
        range_str = '%s - %s' % (date_start, date_end)
        r = re.findall(r'\d\d\d\d', range_str)
        if r and len(set(r)) == 1:
            # If years match, remove the first one
            range_str = re.sub(r'\d\d\d\d', '', range_str, count=1)
        words = range_str.split()
        # Remove recurring months
        range_str = ' '.join(sorted(set(words), key=words.index))
        # Clear multiple whitespaces, add comma before year
        range_str = re.sub(r'\s+', r' ', range_str).strip()
        return re.sub(r'(\s\d\d\d\d)', r',\1', range_str)


class Trip(models.Model):
    BICYCLE = 'bicycle'
    BUS = 'bus'
    CAR = 'car'
    MOTORCYCLE = 'motorcycle'
    PLANE = 'plane'
    SHIP = 'ship'
    TRAIN = 'train'
    WALKING = 'walking'
    OTHER = 'other'

    TYPES = [
        (BICYCLE, 'Bicycle'),
        (SHIP, 'Boat'),
        (BUS, 'Bus'),
        (CAR, 'Car'),
        (MOTORCYCLE, 'Motorcycle'),
        (PLANE, 'Plane'),
        (TRAIN, 'Train'),
        (WALKING, 'Walking'),
        (OTHER, 'Other')
    ]

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="trips")
    display_name = models.CharField(max_length=255)
    type = models.CharField(max_length=13, choices=TYPES, default=PLANE)
    departure_town = models.CharField(max_length=64)
    departure_country = CountryField(blank=True)
    departure_datetime = models.DateTimeField()
    arrival_town = models.CharField(max_length=64)
    arrival_country = CountryField(blank=True)
    arrival_datetime = models.DateTimeField()
    detail1 = models.CharField(max_length=32, blank=True, null=True)
    detail2 = models.CharField(max_length=32, blank=True, null=True)
    towards_party = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="trips", blank=True,
                                   null=True)

    def __str__(self):
        return f'{self.display_name} ({self.departure_town} -> {self.arrival_town})'
