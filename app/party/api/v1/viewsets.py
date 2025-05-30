from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from common.paginations import PageNumberPagination
from party.api.v1.serializers import PartySerializer, TripSerializer

from party.models import Party, Trip


class PartyViewSet(ModelViewSet):
    queryset = Party.objects.select_related("created_by").filter(visible=True)
    serializer_class = PartySerializer
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        scene_id = self.request.data.get("scene_id", None)
        if scene_id:
            serializer.save(created_by=get_user_model().objects.get(scene_id=scene_id))
        else:
            return super().perform_create(serializer)


class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    pagination_class = PageNumberPagination
