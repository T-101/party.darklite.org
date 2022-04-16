from django.core.management.base import BaseCommand
from django.utils import timezone

from party.models import Party


class Command(BaseCommand):
    help = 'Flush parties with no trips, that ended over a month ago'

    def handle(self, *args, **options):
        delta = timezone.localtime() - timezone.timedelta(days=31)
        parties = Party.objects.filter(date_end__lte=delta, trips__isnull=True)
        print(parties)
        # parties.delete()
