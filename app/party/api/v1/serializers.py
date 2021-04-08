from rest_framework.serializers import ModelSerializer

from party.models import Party


class PartySerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'
        # exclude_fields = ["created_by", "id"]
