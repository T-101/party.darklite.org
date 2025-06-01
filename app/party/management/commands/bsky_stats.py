import os
import io

import environ
from atproto import Client, client_utils, models
from PIL import Image, ImageDraw, ImageFont

from config import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from django.template.defaultfilters import pluralize

from party.models import Party, Trip

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))


def create_image(title):
    with Image.open(os.path.join(settings.BASE_DIR, "party/static/images/piggy_template_logo.png")) as im:
        font_path = os.path.join(settings.BASE_DIR, "party/static/party/fonts/adrip1.ttf")
        draw = ImageDraw.Draw(im)
        draw.text((250, 25), "TravelWiki Stats", font=ImageFont.truetype(font_path, 150), fill="black")
        draw.text((200, 280), title, font=ImageFont.truetype(font_path, 100), fill="black")
        buffer = io.BytesIO()
        im.save(buffer, "png")
        buffer.seek(0)
        return buffer, im.size[0], im.size[1]  # Image, width, height


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
        parser.add_argument("-d", "--dry-run", action="store_true", help="Only print the message, don't send it")

    def handle(self, *args, **options):

        if not self.bsky_username or not self.bsky_password:
            return self.stdout.write(self.style.ERROR("BSKY_USERNAME and BSKY_PASSWORD must be set in .env"))

        now = timezone.localtime()

        if options['weekly']:
            delta = now - timezone.timedelta(days=7)
            party_filter = {"created_dt__gte": delta}
            trip_filter = {"created__gte": delta}
            title = "Weekly stats:\n\n"
            image_title = "Weekly\nStats"

        elif options['monthly']:
            delta = now.replace(day=1) - timezone.timedelta(days=1)
            party_filter = {"created_dt__month": delta.month, "created_dt__year": delta.year}
            trip_filter = {"created__month": delta.month, "created__year": delta.year}
            title = f"Monthly stats ({timezone.datetime.strftime(delta, "%b %Y")}):\n\n"
            image_title = timezone.datetime.strftime(delta, "%B %Y").replace(" ", "\n")

        elif options['yearly']:
            delta = now.replace(year=now.year - 1)
            party_filter = {"created_dt__year": delta.year}
            trip_filter = {"created__year": delta.year}
            title = f"Yearly stats ({delta.year}):\n\n"
            image_title = f"Year\n{delta.year}"

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

            if not options['dry_run']:
                img_data, width, height = create_image(image_title)
                msg_bsky = (client_utils.TextBuilder()
                            .text(f'{msg}Go check it out! ')
                            .link('party.darklite.org', 'https://party.darklite.org'))

                client = Client()
                profile = client.login(self.bsky_username, self.bsky_password)
                aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(height=height, width=width)
                post = client.send_image(text=msg_bsky, image=img_data.read(), image_aspect_ratio=aspect_ratio,
                                         image_alt='Darklite Piggy announcing stats for TravelWiki')
                img_data.close()
                stats_title = image_title.replace("\n", " ")
                return self.stdout.write(self.style.SUCCESS(f"Stats for {stats_title} sent to Bluesky: {post.uri}"))
            else:
                text_msg = msg + "Go check it out! https://party.darklite.org"
                return self.stdout.write(self.style.SUCCESS(text_msg))
