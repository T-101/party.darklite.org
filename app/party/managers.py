from django.db import models
from django.utils import timezone


class PartyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("created_by", "modified_by")


class UpcomingPartyManager(models.Manager):
    def get_queryset(self):
        return self.model.objects.select_related("created_by", "modified_by").filter(
            date_end__gte=timezone.now()).order_by('date_start')


class PastPartyManager(models.Manager):
    def get_queryset(self):
        return self.model.objects.select_related("created_by", "modified_by").filter(
            date_end__lt=timezone.now()).order_by('-date_start')
