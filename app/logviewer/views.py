import os
import re
import subprocess

from ipaddress import ip_address

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.views import generic
from django.conf import settings


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

    @staticmethod
    def _readlines_generator(filepath):
        with open(filepath) as raw_data:
            for line in raw_data:
                yield line

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["fail2ban"] = bool(settings.FAIL2BAN_JAILS)
        filepath = os.path.join("/var/log/", self.kwargs.get("filename").lower() + ".log")
        if not os.path.isfile(filepath):
            raise Http404

        regex = re.compile("^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}) - - ")
        lines = ((''.join(regex.findall(x)), x) for x in self._readlines_generator(filepath))
        if self.request.GET.get("search"):
            lines = filter(lambda x: self.request.GET.get("search").lower() in x[1].lower(), lines)
        ctx["file_contents"] = lines
        return ctx

    def post(self, request, *args, **kwargs):
        ip = self.request.POST.get("ban_ip")

        if ip_address(ip.split("/")[0]).is_private:
            return HttpResponse(status=400, content=f"Invalid IP! {ip} belongs to a private IP group")
        command = [
            "echo",
            ip
        ]
        res = subprocess.run(command)
        print("RES", res)
        return HttpResponse(status=200, content=ip)
