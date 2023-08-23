from rest_framework.viewsets import ModelViewSet

from authentication.api.v1.serializers import UserSerializer
from authentication.models import User
from common.permissions import IsSuperUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
