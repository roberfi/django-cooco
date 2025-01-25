from collections.abc import Iterable

from django import template
from django.http import HttpRequest

from django_cooco.models import BannerConfig, CookieGroup
from django_cooco.utils import CooCoManager

register = template.Library()


@register.simple_tag
def get_cooco_banner_config() -> BannerConfig:
    return BannerConfig.get_solo()


@register.simple_tag
def get_cookie_groups() -> Iterable[CookieGroup]:
    return CookieGroup.objects.all()  # type: ignore[attr-defined]


@register.simple_tag
def get_cooco_manager(request: HttpRequest) -> CooCoManager:
    return CooCoManager.from_request(request)


@register.filter
def ask_for_cooco(cooco_manager: CooCoManager) -> bool:
    return cooco_manager.is_cooco_outdated()


@register.filter
def is_cookie_group_accepted(cooco_manager: CooCoManager, cookie_group: CookieGroup) -> bool:
    return cookie_group.is_required or cooco_manager.is_cookie_group_accepted(cookie_group.cookie_id)


@register.filter
def any_optional_cookie_group(cookie_groups: Iterable[CookieGroup]) -> bool:
    return any(cookie_group for cookie_group in cookie_groups if not cookie_group.is_required)
