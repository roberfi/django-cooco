from django.urls import path

from django_cooco.views import AcceptAllCookies, SetCookiePreferences

urlpatterns = (
    path("accept-all", AcceptAllCookies.as_view(), name="accept_all_cookies"),
    path("set-preferences", SetCookiePreferences.as_view(), name="set_cookie_preferences"),
)
