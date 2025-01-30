from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    def get(self, request):
        from authentication.api.v1.serializers import MeSerializer  # avoid circular import
        return Response(MeSerializer(request.user).data)
