from rest_framework.routers import SimpleRouter

from party.api.v1.viewsets import PartyViewSet

router = SimpleRouter()

router.register('parties', PartyViewSet, basename="parties")
