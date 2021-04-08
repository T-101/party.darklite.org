from rest_framework.routers import SimpleRouter

from authentication.api.v1.viewsets import UserViewSet

router = SimpleRouter()

router.register('users', UserViewSet)
