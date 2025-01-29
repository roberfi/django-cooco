# django-cooco

django-cooco is a Django app to manage cookie consent in Django projects. This library was inspired by [django-cookie-consent](https://github.com/jazzband/django-cookie-consent), which I have taken as referece to create a simplier and more customizable solution.

## Quick start

1. Add "django_cooco" to your `INSTALLED_APPS` setting like this:
    ```python
        INSTALLED_APPS = [
            ...,
            "django_cooco",
        ]
    ```

2. Include the django_cooco URLconf in your project `urls.py` like this:   

    ```python
    urlpatterns = (
        ...,
        path("cooco/", include("django_cooco.urls")),
    )
    ```

3. Run `python manage.py migrate` to create the models.

## Settings
You can configure the following settings in your project `settings.py` file:

| Setting                | Type  | Definition                                                      | Mandatory | Default value       |
| ---------------------- | ----- | --------------------------------------------------------------- | --------- | ------------------- |
| `COOCO_COOKIE_NAME`    | `str` | Name of the cookie to store the cookie consent status           | False     | `"cooco"`           |
| `COOCO_COOKIE_MAX_AGE` | `int` | Max age of the cookie where the cookie consent status is stored | False     | `31536000` (1 year) |

## Database 
### Models

#### `BannerConfig`
A singleton model to configure the cookie consent banner title and text:

| Field         | Type           | Definition                                           |
| ------------- | -------------- | ---------------------------------------------------- |
| `title`       | `CharField`    | Title of the cookie consent banner                   |
| `text`        | `CharField`    | Text to show in the cookie consent banner            |
| `show_banner` | `BooleanField` | Whether cookie consent banner should be shown or not |

#### `CookieGroup`
The model to set the groups of cookies that will be used by the web:

| Field         | Type                      | Definition                                                                                                           |
| ------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `cookie_id`   | `CharField`               | Unique id of the cookie group                                                                                        |
| `name`        | `CharField`               | Human readable name of the cookie group                                                                              |
| `description` | `TextField`               | Description of the cookies of that cookie group                                                                      |
| `is_required` | `BooleanField`            | Whether the cookie group is required or optional                                                                     |
| `version`     | `PositiveBigIntegerField` | Non-editable version of the cookie group object. It will be automatically increased after every saving of the model. |

### Database Relationships
To use optional cookies, you could add a `ForeignKey` field to your cookie consent dependent model. For example:
```python
from django.db import models
from django_cooco.models import CookieGroup


class GoogleAnalytics(models.Model):
    gtag = models.CharField(max_length=20)
    cookie_consent = models.ForeignKey(CookieGroup, on_delete=models.RESTRICT)

    def __str__(self):
        return "Google Analytics"

```

## Tags and filters
To use them you need to load `cooco` tags:
```
{% load cooco %}
```

### Tags
#### `get_cooco_banner_config`

Returns the needed data to display the cookie consent banner.

**Returns:**
- (`BannerConfig`): the data stored in the BannerConfig database model.

**Usage example:**
```html
{% get_cooco_banner_config as banner %}
{% if banner.show_banner %}
    <div id="cooco_banner">
        <div>
            <h2>
                {{ banner.title }}
            </h2>
            <p>
                {{ banner.text }}
            </p>
        </div>
    </div>
{% endif %}
```
    
#### `get_cookie_groups`

Returns the data of the configured cookie groups.

**Returns:**
- (`Iterable[CookieGroup]`): the data stored in the CookieGroup database model.

**Usage example:**
```
{% get_cookie_groups as cookie_groups %}
```

#### `get_cooco_manager`

Returns the status of the cookie consent in the request to the server.

**Arguments:**
- `request` (`HttpRequest`): the request to the server.

**Returns:**
- (`CooCoManager`): object containing the status of the cookie consent built from the request that can be used in some filters (see below).

**Usage example:**
```
{% get_cooco_manager request as cooco_manager %}
```

### Filters
#### `ask_for_cooco`

Checks whether the cookie consent banner should be shown or not giving the object returned from `get_cooco_manager` tag.

**Arguments:**
- `cooco_manager` (`CooCoManager`): object containing the status of the cookie consent.

**Returns:**
- (`bool`): whether the cookie consent banner should be shown or not.

**Usage example:**
```
{% if cooco_manager|ask_for_cooco %}
    ...
{% endif %}
```

#### `is_cookie_group_accepted`

Checks whether the given cookie group is accepted by the user or not giving the object returned from `get_cooco_manager` tag.

**Arguments:**
- `cooco_manager` (`CooCoManager`): object containing the status of the cookie consent.
- `cookie_group` (`CookieGroup`): cookie group to check.

**Returns:**
- (`bool`): whether the given cookie group is accepted by the user or not.

**Usage example:**
```
{% if cooco_manager|is_cookie_group_accepted:cookie_consent %}
    ...
{% endif %}
```

#### `any_optional_cookie_group`

Checks if any of the given cookies is optional. This could be useful if you have to display a settings button or just "accept" option.

**Arguments:**
- `cookie_groups` (`Iterable[CookieGroup]`): iterable of cookie groups to check.

**Returns:**
- (`bool`): where there is any optional cookie group or not.

**Usage example:**
```
{% if cookie_groups|any_optional_cookie_group %}
    ...
{% endif %}
```

## URLs
#### `POST 'set_cookie_preferences'`
Set cookie preferences.

**Request fields:**
| Field                              | Type  | Definition                            |
| ---------------------------------- | ----- | ------------------------------------- |
| `next`                             | `str` | Path to redirect when request is sent |
| cookie_id* (additional properties) | `str` | "on" if accepted, otherwise rejected  |

**Example:**
```json
{
    "next": "/home",
    "analytics": "on",
    "ads": "off",
}
```

#### `POST 'accept_all_cookies'`
Accept all cookies.

**Request fields:**
| Field  | Type  | Definition                            |
| ------ | ----- | ------------------------------------- |
| `next` | `str` | Path to redirect when request is sent |

**Example:**
```json
{
    "next": "/home",
}
```

## Full example
Here you can see an example of how the full functionality implementation could look like. Note that `"analytics"` entry is present in the template context, which contains a database entry with a `ForeignKey` field to `CookieGroup` table called `"cookie_consent"` (see "Database Relationships" section of this document).

```html
{% load cooco %}

{% get_cooco_manager request as cooco_manager %}

<!DOCTYPE html>
<html>
    <head>
        <title>Cooco Example</title>

        {% if cooco_manager|is_cookie_group_accepted:analytics.cookie_consent %}
            <script>
                // Script to use Analytics
            </script>
        {% endif %}
    </head>

    <body>
        <p>This is an example of Cooco usage</p>

        {% if cooco_manager|ask_for_cooco %}
            {% get_cooco_banner_config as banner %}
            
            {% if banner.show_banner %}
                <div id="cooco_banner">
                    <div>
                        <h2>
                            {{ banner.title }}
                        </h2>
                        <p>
                            {{ banner.text }}
                        </p>

                        {% get_cookie_groups as cookie_groups %}
                        
                        {% if cookie_groups|any_optional_cookie_group %}
                            <button onclick="showCookiesModal()">Settings</button>
                            <dialog>
                                <form class="inline-block"
                                    action="{% url 'set_cookie_preferences' %}"
                                    method="post">
                                    {% csrf_token %}
                                    <input name="next" type="hidden" value="{{ request.path }}" />
                                    {% for cookie_group in cookie_groups %}
                                        <div>
                                            <h1>
                                                {{ cookie_group.name }}
                                            </h1>
                                            <p>
                                                {{ cookie_group.description }}
                                            </p>
                                            <input name="{{ cookie_group.cookie_id }}"
                                                type="checkbox"
                                                checked="checked"
                                                {% if cookie_group.is_required %}disabled{% endif %} />
                                        </div>
                                    {% endfor %}
                                    <button type="submit">Save</button>
                                </form>
                            </dialog> 
                        {% endif %}
                        
                        <form class="inline-block"
                            action="{% url 'accept_all_cookies' %}"
                            method="post">
                            {% csrf_token %}
                            <input name="next" type="hidden" value="{{ request.path }}">
                            <button type="submit">Accept</button>
                        </form>
                    </div>
                </div>
            {% endif %}
        
        {% endif %}

    </body>

</html>
```
