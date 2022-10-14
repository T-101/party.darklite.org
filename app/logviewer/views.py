import os

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.views import generic


class AdminBaseView(UserPassesTestMixin, generic.TemplateView):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        raise Http404


class LogViewerIndexView(AdminBaseView):
    template_name = 'logviewer/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["files"] = sorted(
            [(os.path.splitext(x)[0].capitalize(), os.stat(os.path.join("/var/log/", x)).st_size) for x in
             os.listdir("/var/log/") if x.endswith(".log")])
        return ctx


class LogViewerDetailView(AdminBaseView):
    template_name = "logviewer/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        filepath = os.path.join("/var/log/", self.kwargs.get("filename").lower() + ".log")
        try:
            with open(filepath) as raw_data:
                ctx["file_contents"] = raw_data.readlines()
        except FileNotFoundError:
            raise Http404
        return ctx
