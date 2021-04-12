import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.views import generic, View
from django.conf import settings
from django.views.generic import RedirectView


class DisplayNameView(generic.TemplateView):
    template_name = 'authentication/display_name.html'


class AuthView(generic.TemplateView):
    template_name = 'authentication/display_name.html'


class SceneIDAuthRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.request.session['sceneid_state'] = get_random_string(length=32)
        params = {
            'client_id': settings.SCENEID_CLIENT_ID,
            'redirect_uri': settings.SCENEID_RETURN_BASE_URL + reverse('authentication:sceneid_return'),
            'response_type': 'code',
            'state': self.request.session['sceneid_state']
        }
        url = settings.SCENEID_HOST + '/oauth/authorize/?' + urllib.parse.urlencode(params)
        return url


class SceneIDAuthReturn(View):
    def get(self, request, *args, **kwargs):
        state, code = map(self.request.GET.get, ['state', 'code'])

        try:
            session_state = request.session['sceneid_state']
        except KeyError:
            messages.info(request, "Something went wrong, please try again (Error 1)")
            return redirect("party:landing_page")
        del request.session['sceneid_state']

        if state != session_state:
            messages.info(request, "Something went wrong, please try again (Error 2)")
            return redirect("party:landing_page")

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SCENEID_RETURN_BASE_URL + reverse('authentication:sceneid_return'),
        }

        response_data = requests.post(
            url=settings.SCENEID_HOST + '/oauth/token/',
            data=data,
            auth=HTTPBasicAuth(settings.SCENEID_CLIENT_ID, settings.SCENEID_SECRET)
        ).json()

        headers = {'Authorization': f'Bearer {response_data.get("access_token")}'}

        response_data = requests.get(url=settings.SCENEID_HOST + '/api/3.0/me/', headers=headers).json()
        payload = response_data.get('user')

        try:
            user = get_user_model().objects.get(scene_id=payload["id"])
        except get_user_model().DoesNotExist:
            user = None

        error_msg = "Your account has been disabled. If you feel that this is wrong, contact the administrator"
        if user is not None and not user.is_active:
            messages.warning(self.request, error_msg)
            return redirect('party:landing_page')

        if user is not None and user.is_active:
            # we have a known active local user linked to this sceneid
            login(request, user)
        else:
            username = slugify(payload['display_name'], allow_unicode=False)
            user = get_user_model().objects.create_user(
                email=f"{username}@sceneid.{payload['id']}",
                display_name=payload['display_name'],
                scene_id=payload["id"]
            )
            login(request, user)
            messages.success(self.request, "Account created successfully!")

        return redirect('party:landing_page')
