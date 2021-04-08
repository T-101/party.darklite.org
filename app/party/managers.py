from django.db import models
from django.utils import timezone


class UpcomingPartyManager(models.Manager):
    def get_queryset(self):
        return self.model.objects.filter(date_end__gte=timezone.now()).order_by('date_start')


class PastPartyManager(models.Manager):
    def get_queryset(self):
        return self.model.objects.filter(date_end__lt=timezone.now()).order_by('-date_start')
