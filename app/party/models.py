import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField

from party.managers import UpcomingPartyManager, PastPartyManager


class Party(models.Model):
    name = models.CharField(max_length=64)
    date_start = models.DateField()
    date_end = models.DateField()
    location = models.CharField(max_length=64)
    country = CountryField(multiple=False, null=True, blank=True)
    www = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=True)

    created_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Created datetime')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)

    objects = models.Manager()
    upcoming_parties = UpcomingPartyManager()
    past_parties = PastPartyManager()

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"

    def save(self, *args, **kwargs):
        slug = slugify('%s %s' % (self.name, self.date_start.year))
        self.slug = re.sub(r'-(\d{4})(?=.+\1)', '', slug)
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
    BUS = 'bus'
    CAR = 'car'
    MOTORCYCLE = 'motorcycle'
    PLANE = 'plane'
    SHIP = 'ship'
    TRAIN = 'train'
    OTHER = 'other'

    TYPES = [
        (SHIP, 'Boat'),
        (BUS, 'Bus'),
        (CAR, 'Car'),
        (MOTORCYCLE, 'Motorcycle'),
        (PLANE, 'Plane'),
        (TRAIN, 'Train'),
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
    towards_home = models.BooleanField(default=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="trips", blank=True, null=True)

    def __str__(self):
        return '%s -> %s' % (self.departure_town, self.arrival_town)
