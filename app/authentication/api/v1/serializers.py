from authentication.models import User
from common.serializers import BaseModelSerializer


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'first_name', 'last_name', 'id']
