from django.urls import reverse
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from authentication.api.v1.serializers import UserSerializer
from common.serializers import BaseModelSerializer
from party.models import Party, Trip


class PartySerializer(BaseModelSerializer):
    created_by = UserSerializer(fields=["display_name"])
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            return f"{request.scheme}://{request.get_host()}{reverse('party:detail', args=[obj.slug])}"

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


class TripSerializer(CountryFieldMixin, BaseModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
