from rest_framework import serializers

from authentication.models import User
from common.serializers import BaseModelSerializer
import party.api.v1.serializers as party_serializers  # avoid circular import
from party.models import Party


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'first_name', 'last_name', 'id']


class MeSerializer(UserSerializer):
    api_token = serializers.CharField(source='auth_token.key', read_only=True)
    share_code = serializers.CharField(source='share.short_uuid', read_only=True)
    parties_added = serializers.SerializerMethodField()
    trips = serializers.SerializerMethodField()

    def get_trips(self, obj):
        serializer = party_serializers.TripSerializer(obj.trips.all(), many=True)
        return serializer.data

    def get_parties_added(self, obj):
        serializer = party_serializers.PartySerializer(Party.objects.filter(created_by=obj), many=True,
                                                       context=self.context,
                                                       exclude_fields=["modified_by", "id"])
        return serializer.data

    class Meta(UserSerializer.Meta):
        exclude = UserSerializer.Meta.exclude + ['email', 'scene_id', 'is_active', 'is_staff', 'is_superuser']
