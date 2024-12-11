import os

import environ
from atproto import Client, client_utils

from config import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from django.template.defaultfilters import pluralize

from party.models import Party, Trip

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))


class Command(BaseCommand):
    help = 'Send stats to Bluesky'

    def __init__(self):
        super().__init__()
        self.bsky_username = env.str('BSKY_USERNAME', "")
        self.bsky_password = env.str('BSKY_PASSWORD', "")

    def add_arguments(self, parser):
        parser.add_argument("-w", "--weekly", action="store_true", help="Get stats from past 7 days")
        parser.add_argument("-m", "--monthly", action="store_true", help="Get stats from previous month")
        parser.add_argument("-y", "--yearly", action="store_true", help="Get stats from previous year")
        parser.add_argument("-d", "--debug", action="store_true", help="Post to bsky in debug mode")

    def handle(self, *args, **options):

        if not self.bsky_username or not self.bsky_password:
            return self.stdout.write(self.style.ERROR("BSKY_USERNAME and BSKY_PASSWORD must be set in .env"))

        now = timezone.localtime()

        if options['weekly']:
            delta = now - timezone.timedelta(days=7)
            party_filter = {"created_dt__gte": delta}
            trip_filter = {"created__gte": delta}
            title = "Weekly stats:\n\n"

        elif options['monthly']:
            delta = now.replace(month=now.month - 1)
            party_filter = {"created_dt__month": delta.month, "created_dt__year": delta.year}
            trip_filter = {"created__month": delta.month, "created__year": delta.year}
            title = f"Monthly stats ({timezone.datetime.strftime(delta, "%b %Y")}):\n\n"

        elif options['yearly']:
            delta = now.replace(year=now.year - 1)
            party_filter = {"created_dt__year": delta.year}
            trip_filter = {"created__year": delta.year}
            title = f"Yearly stats ({delta.year}):\n\n"

        else:
            return self.stdout.write(self.style.NOTICE("Please provide either -w, -m or -y parameter"))

        parties = (Party.objects.filter(**party_filter)
                   .aggregate(party_count=Count("pk"), user_count=Count("created_by", distinct=True)))
        trips = (Trip.objects.filter(**trip_filter, towards_party=True)
                 .aggregate(trip_count=Count("pk", distinct=True), user_count=Count("created_by", distinct=True)))

        msg = ""

        if sum(parties.values()) > 0:
            pc, uc = parties['party_count'], parties['user_count']
            msg += f"{pc} part{pluralize(pc, "y,ies")} added by {uc} user{pluralize(uc)}\n\n"

        if sum(trips.values()) > 0:
            tc, uc = trips['trip_count'], trips['user_count']
            msg += f"{tc} trip{pluralize(tc)} towards parties added by {uc} user{pluralize(uc)}\n\n"

        if msg:
            msg = "Travelwiki " + title + msg

            if not settings.DEBUG or options['debug']:
                msg_bsky = (client_utils.TextBuilder()
                          .text(f'{msg}Go check it out! ')
                          .link('party.darklite.org', 'https://party.darklite.org'))

                client = Client()
                profile = client.login(self.bsky_username, self.bsky_password)
                post = client.send_post(msg_bsky)


            text_msg = msg + "Go check it out! https://party.darklite.org"
            return self.stdout.write(self.style.SUCCESS(text_msg))


