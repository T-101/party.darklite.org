from django.views.generic import TemplateView


class FeedsView(TemplateView):
    template_name = 'party/feeds.html'
