from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed, RssUserland091Feed, Atom1Feed

from party.models import Party


class BasePartyFeed(Feed):
    title = "Darklite Partywiki Parties"
    link = "https://party.darklite.org/"
    description = "You'll never travel alone - Even if you'd want to!"

    def get_feed(self, obj, request):
        # Since we are running behind a reverse proxy, we need to tell Django that we are running on HTTPS
        # when in production. This is because the reverse proxy is handling the SSL termination.
        request.is_secure = lambda: not settings.DEBUG

        feed = super().get_feed(obj, request)
        if settings.DEBUG:
            feed.content_type = 'text/xml; charset=utf-8'
        return feed

    def items(self):
        return Party.objects.filter(visible=True).order_by('-created_dt')[:10]

    def item_title(self, item):
        return item

    def author_name(self):
        return "Darklite Partywiki"

    def item_description(self, item):
        return f"{item.date_range} - {item.location}, {item.country.name}"

    def item_pubdate(self, item):
        return item.created_dt

    def item_updateddate(self, item):
        return item.modified_dt

    def item_link(self, item):
        return reverse('party:detail', args=[item.slug])


class PartyFeedRss2(BasePartyFeed):
    feed_type = Rss201rev2Feed


class PartyFeedRss09(BasePartyFeed):
    feed_type = RssUserland091Feed


class PartyFeedAtom1(BasePartyFeed):
    feed_type = Atom1Feed
