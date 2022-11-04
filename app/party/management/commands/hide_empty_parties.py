from django.core.management.base import BaseCommand
from django.utils import timezone

from party.models import Party


class Command(BaseCommand):
    help = 'Hide parties with no trips, that ended over a month ago'

    def handle(self, *args, **options):
        delta = timezone.localtime() - timezone.timedelta(days=31)
        parties = Party.objects.filter(date_end__lte=delta, trips__isnull=True)
        if len(parties):
            print(f"Hiding {len(parties)} parties.")
            parties.update(visible=False)
        else:
            print("Nothing to hide.")
