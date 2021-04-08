from django.http import HttpResponseForbidden


class AuthenticatedOr403Mixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)
