from collections.abc import Iterable

from django import template
from django.http import HttpRequest

from django_cooco.models import BannerConfig, CookieGroup
from django_cooco.utils import CookieConsentManager

register = template.Library()


@register.simple_tag
def get_cookie_consent_manager(request: HttpRequest) -> CookieConsentManager:
    return CookieConsentManager.from_request(request)


@register.simple_tag
def get_cookie_consent_banner() -> BannerConfig:
    return BannerConfig.get_solo()


@register.simple_tag
def get_cookie_groups() -> Iterable[CookieGroup]:
    return CookieGroup.objects.all()  # type: ignore[attr-defined]


@register.filter
def ask_for_cookie_consent(cookie_consent_manager: CookieConsentManager) -> bool:
    return cookie_consent_manager.is_any_cookie_consent_outdated()


@register.filter
def is_cookie_group_accepted(cookie_consent_manager: CookieConsentManager, cookie_group: CookieGroup | None) -> bool:
    if cookie_group is None:
        return False

    return cookie_group.is_required or cookie_consent_manager.is_cookie_group_accepted(cookie_group.cookie_id)


@register.filter
def any_optional_cookie_group(cookie_groups: Iterable[CookieGroup]) -> bool:
    return any(cookie_group for cookie_group in cookie_groups if not cookie_group.is_required)
