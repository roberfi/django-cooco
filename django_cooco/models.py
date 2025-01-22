from django.db import models
from solo.models import SingletonModel


class BannerConfig(SingletonModel):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    title = models.CharField(max_length=100, unique=True)
    text = models.CharField(max_length=200)
    show_banner = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Cookie consent banner"


class CookieGroup(models.Model):  # type: ignore[django-manager-missing] # https://github.com/typeddjango/django-stubs/issues/1023
    cookie_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_required = models.BooleanField()
    version = models.PositiveBigIntegerField(default=0, editable=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.version += 1
        super().save(*args, **kwargs)
