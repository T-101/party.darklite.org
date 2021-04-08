from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'first_name', 'last_name', 'id']
