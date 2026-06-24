from django.urls import path

from django_cooco.views import AcceptAllCookies, RejectAllCookies, SetCookiePreferences

urlpatterns = (
    path("accept-all", AcceptAllCookies.as_view(), name="accept_all_cookies"),
    path("reject-all", RejectAllCookies.as_view(), name="reject_all_cookies"),
    path("set-preferences", SetCookiePreferences.as_view(), name="set_cookie_preferences"),
)
