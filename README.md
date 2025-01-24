# django-cooco

django-cooco is a Django app to manage cookie consent in Django projects.

## Quick start

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_cooco",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("cooco/", include("django_cooco.urls")),

3. Run ``python manage.py migrate`` to create the models.

## Settings
You can configure the following settings in your project `settings.py` file:

| Setting                | Type  | Definition                                                      | Mandatory | Default value       |
| ---------------------- | ----- | --------------------------------------------------------------- | --------- | ------------------- |
| `COOCO_COOKIE_NAME`    | `str` | Name of the cookie to store the cookie consent status           | False     | `"cooco"`           |
| `COOCO_COOKIE_MAX_AGE` | `int` | Max age of the cookie where the cookie consent status is stored | False     | `31536000` (1 year) |