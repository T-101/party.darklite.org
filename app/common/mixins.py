from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.urls import reverse


class AuthenticatedOr403Mixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def get_login_url(self):
        return reverse("authentication:auth")
