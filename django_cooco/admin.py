from django.contrib.admin import ModelAdmin, register
from solo.admin import SingletonModelAdmin

from django_cooco.models import BannerConfig, CookieGroup


@register(BannerConfig)
class BannerConfigAdmin(SingletonModelAdmin):
    pass


@register(CookieGroup)
class CookieGroupAdmin(ModelAdmin):
    readonly_fields = ("version",)
