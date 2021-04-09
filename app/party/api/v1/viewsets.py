from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from party.api.v1.serializers import PartySerializer

from party.models import Party


class PartyViewSet(ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def perform_create(self, serializer):
        scene_id = self.request.data.get("scene_id", None)
        if scene_id:
            serializer.save(created_by=get_user_model().objects.get(scene_id=scene_id))
        else:
            return super().perform_create(serializer)
