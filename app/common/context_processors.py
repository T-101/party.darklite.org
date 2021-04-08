from django.conf import settings


def google_analytics(request):
    return {
        'ga_tag': settings.GOOGLE_ANALYTICS or None
    }
