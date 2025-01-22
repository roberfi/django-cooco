============
django-cooco
============

django-cooco is a Django app to manage cookie consent in Django projects.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "django_cooco",
    ]

2. Include the polls URLconf in your project urls.py like this::

    path("cooco/", include("django_cooco.urls")),

3. Run ``python manage.py migrate`` to create the models.
