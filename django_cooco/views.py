from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.base import View

from django_cooco.utils import CooCoManager


class SetCookiesBaseView(View, ABC):
    @staticmethod
    def _set_cookie_and_redirect(request: HttpRequest, cookie_group_statuses: CooCoManager) -> HttpResponseRedirect:
        return cookie_group_statuses.set_cooco_cookie(HttpResponseRedirect(request.POST.get("next", "/")))

    @abstractmethod
    def post(self, request: HttpRequest) -> HttpResponseRedirect: ...


class AcceptAllCookies(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookie_and_redirect(request, CooCoManager.all_cookies_accepted())


class SetCookiePreferences(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookie_and_redirect(request, CooCoManager.parse_cooco_form(request.POST))
