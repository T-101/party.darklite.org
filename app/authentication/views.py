from django.views import generic


class DisplayNameView(generic.TemplateView):
    template_name = 'authentication/display_name.html'


class AuthView(generic.TemplateView):
    template_name = 'authentication/display_name.html'
