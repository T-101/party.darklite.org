from rest_framework.viewsets import ModelViewSet

from party.api.v1.serializers import PartySerializer

from party.models import Party


class PartyViewSet(ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
