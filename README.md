# django-cooco

django-cooco is a Django app to manage cookie consent in Django projects. This library was inspired by [django-cookie-consent](https://github.com/jazzband/django-cookie-consent), which I have taken as referece to create a simplier and more customizable solution.

## Quick start

1. Add "polls" to your `INSTALLED_APPS` setting like this:
    ```python
        INSTALLED_APPS = [
            ...,
            "django_cooco",
        ]
    ```

2. Include the polls URLconf in your project `urls.py` like this:   

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

## Full example

Here you can see an example of how the full functionality implementation could look like. Note that you would need "my_table_content" in the template context, which is a database entry that contains a ForeignKey field called "cookie_consent" to CookieGroup.

```html
{% load cooco %}

{% get_cooco_manager request as cooco_manager %}

<!DOCTYPE html>
<html>
    <head>
        <title>Cooco Example</title>

        {% if cooco_manager|is_cookie_group_accepted:my_table_content.cookie_consent %}
            <script>
                // Script that stores the cookies that the user has accepted
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
                                    </div>
                                {% endfor %}
                                <button type="submit">Save</button>
                            </dialog> 
                        {% endif %}
                        
                        <button>Accept</button>
                    </div>
                </div>
            {% endif %}
        
        {% endif %}

    </body>

</html>
```
