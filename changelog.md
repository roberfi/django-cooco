# Changelog

## 0.1.0

- Add `RejectAllCookies` view and `reject-all` URL to allow wiring up a "Reject all" button
- Add `httponly=True` to `CooCoManager.set_cooco_cookie` for improved security
- Add `COOCO_COOKIE_SECURE` setting (default `False`) to control the `secure` flag on the consent cookie
- Add `CooCoManager.all_cookies_rejected()` classmethod

## 0.0.1

- First release
