from authentication.api.v1.serializers import UserSerializer
from common.serializers import BaseModelSerializer
from party.models import Party


class PartySerializer(BaseModelSerializer):

    created_by = UserSerializer(fields=["display_name"])

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data.get("country"):
            # Failsafe if country is missing in ie. legacy data
            data["country"] = None
        return data

    class Meta:
        model = Party
        fields = '__all__'
        # exclude_fields = ["created_by", "id"]
