import base64

import requests
import urllib.parse
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core.exceptions import SuspiciousOperation
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
            # The trailing slash was throwing id.scene.org off... so we clip it out with [:-1]
            'redirect_uri': settings.SCENEID_RETURN_BASE_URL + reverse('authentication:sceneid_return')[:-1],
            'response_type': 'code',
            'state': self.request.session['sceneid_state']
        }
        url = settings.SCENEID_HOST + '/oauth/authorize/?' + urllib.parse.urlencode(params)
        print("REDIRECT URL", url)
        print("PAYLOAD REDIRECT URL", params.get("redirect_uri"))
        return url


class SceneIDAuthReturn(View):
    def get(self, request, *args, **kwargs):
        state, code = map(self.request.GET.get, ['state', 'code'])

        # This maybe helps with the occational "State mismatch" errors
        session_state = request.session['sceneid_state']
        del request.session['sceneid_state']

        print("PIERPIERPIERPEIRPIEPRIEPIR", settings.SCENEID_RETURN_BASE_URL + reverse('authentication:sceneid_return')[:-1])

        if state != session_state:
            raise SuspiciousOperation("State mismatch!")

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            # Again we strip the trailing slash from the url with [:-1]
            'redirect_uri': settings.SCENEID_RETURN_BASE_URL + reverse('authentication:sceneid_return')[:-1],
        }

        headers = {
            'Authorization': "Basic " + base64.b64encode(
                bytes(settings.SCENEID_CLIENT_ID + ":" + settings.SCENEID_SECRET, encoding='utf-8')).decode('utf-8'),
        }
        response_data = requests.post(url=settings.SCENEID_HOST + '/oauth/token/', data=data, headers=headers).json()

        headers = {'Authorization': f'Bearer {response_data.get("access_token")}'}

        response_data = requests.get(url=settings.SCENEID_HOST + '/api/3.0/me/', headers=headers).json()
        payload = response_data.get('user')

        try:
            user = get_user_model().objects.get(visitor__sceneid_user_id=payload["id"])
        except get_user_model().DoesNotExist:
            user = None

        error_msg = "Your account has been disabled. If you feel that this is wrong, contact the administrator"
        if user is not None and not user.is_active:
            messages.error(request, error_msg)
            return redirect('www:landingpage')

        if user is not None and user.is_active:
            # we have a known active local user linked to this sceneid
            login(request, user)
        else:
            username = slugify(payload['display_name'], allow_unicode=False)
            visitor = create_visitor(username=username, nickname=payload['display_name'], scene_id=payload['id'])
            login(request, visitor.user)
            messages.add_message(self.request, messages.INFO, "Account created successfully!")

        return redirect('www:landingpage')
