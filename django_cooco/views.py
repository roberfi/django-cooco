from abc import ABC, abstractmethod

from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.base import View

from django_cooco.utils import CookieConsentManager


class SetCookiesBaseView(View, ABC):
    @staticmethod
    def _set_cookie_and_redirect(
        request: HttpRequest, cookie_group_statuses: CookieConsentManager
    ) -> HttpResponseRedirect:
        return cookie_group_statuses.set_cookie_consent_cookie(HttpResponseRedirect(request.POST.get("next", "/")))

    @abstractmethod
    def post(self, request: HttpRequest) -> HttpResponseRedirect: ...


class AcceptAllCookies(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookie_and_redirect(request, CookieConsentManager.all_cookies_accepted())


class SetCookiePreferences(SetCookiesBaseView):
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        return self._set_cookie_and_redirect(request, CookieConsentManager.parse_cookie_consent_form(request.POST))
