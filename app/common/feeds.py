from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed, RssUserland091Feed, Atom1Feed

from party.models import Party


class BaseAddElementsFeed:
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement(u"country", item['country'])
        handler.addQuickElement(u"location", item['location'])
        handler.addQuickElement(u"partyStart", item['partyStart'])
        handler.addQuickElement(u"partyStartStr", item['partyStartStr'])
        handler.addQuickElement(u"partyEnd", item['partyEnd'])
        handler.addQuickElement(u"partyEndStr", item['partyEndStr'])
        handler.addQuickElement(u"partyUrl", item['partyUrl'])


class ExtendedRss201rev2Feed(BaseAddElementsFeed, Rss201rev2Feed):
    pass


class ExtendedRssUserland091Feed(BaseAddElementsFeed, RssUserland091Feed):
    pass


class ExtendedAtom1Feed(BaseAddElementsFeed, Atom1Feed):
    pass


class BasePartyFeed(Feed):
    title = "Partywiki Parties"
    link = "/feeds/"
    description = "Partywiki Parties Description"

    def get_feed(self, obj, request):
        feed = super().get_feed(obj, request)
        if settings.DEBUG:
            feed.content_type = 'text/xml; charset=utf-8'
        else:
            feed.content_type = 'application/rss+xml; charset=utf-8'
        return feed

    def items(self):
        return Party.objects.order_by('-created_dt')[:10]

    def item_extra_kwargs(self, item):
        return {
            "country": item.country.name,
            "location": item.location,
            "partyStart": item.date_start.isoformat(),
            "partyStartStr": item.date_start.strftime("%a %b %-d %Y"),
            "partyEnd": item.date_end.isoformat(),
            "partyEndStr": item.date_end.strftime("%a %b %-d %Y"),
            "partyUrl": item.www
        }

    def item_title(self, item):
        return item.name

    def item_pubdate(self, item):
        return item.created_dt

    def item_link(self, item):
        return reverse('party:detail', args=[item.slug])


class PartyFeedRss2(BasePartyFeed):
    feed_type = ExtendedRss201rev2Feed
    link = "/feeds/parties_rss2.xml"


class PartyFeedRss09(BasePartyFeed):
    feed_type = ExtendedRssUserland091Feed
    link = "/feeds/parties_rss09.xml"


class PartyFeedAtom1(BasePartyFeed):
    feed_type = ExtendedAtom1Feed
    link = "/feeds/parties_atom1.xml"
