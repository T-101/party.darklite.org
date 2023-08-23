"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from party.api.v1.routers import router as v1_party_router
from authentication.api.v1.routers import router as v1_authentication_router
from party.views.feeds import FeedsView
from common.feeds import PartyFeedRss2, PartyFeedRss09, PartyFeedAtom1

v1router = routers.DefaultRouter() if settings.DEBUG else routers.SimpleRouter()

v1router.registry.extend(v1_party_router.registry)
if settings.DEBUG:
    v1router.registry.extend(v1_authentication_router.registry)

urlpatterns = [
    path('autocomplete/', include('autocomplete_contrib.urls')),
    path('admin/', admin.site.urls),
    path('feeds/', FeedsView.as_view(), name="feeds"),
    path('feeds/parties_rss2.xml', PartyFeedRss2(), name="feeds-rss2"),
    path('feeds/parties_rss09.xml', PartyFeedRss09(), name="feeds-rss09"),
    path('feeds/parties_atom1.xml', PartyFeedAtom1(), name="feeds-atom1"),
    path('api/v1/', include(v1router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('logviewer/', include('logviewer.urls')),
    path('account/', include('authentication.urls')),
    path('', include('party.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    # This will enable static assets even when debugging using gunicorn etc
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
