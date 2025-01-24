import json
from collections.abc import Iterable, Sequence
from typing import Any, NamedTuple, TypeVar

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from typing_extensions import Self

from django_cooco.models import CookieGroup

THttpResponse = TypeVar("THttpResponse", bound=HttpResponse)


class CooCoStatus(NamedTuple):
    version: int
    is_accepted: bool


class CooCo(NamedTuple):
    cookie_id: str
    current_version: int
    cooco_status: CooCoStatus

    @property
    def is_version_outdated(self) -> bool:
        return self.current_version != self.cooco_status.version

    @property
    def is_accepted(self) -> bool:
        return not self.is_version_outdated and self.cooco_status.is_accepted


class CooCoManager:
    COOCO_COOKIE_NAME = getattr(settings, "COOCO_COOKIE_NAME", "cooco")
    COOCO_COOKIE_MAX_AGE = getattr(settings, "COOCO_COOKIE_MAX_AGE", 60 * 60 * 24 * 365 * 1)
    DEFAULT_COOCO_STATUS = CooCoStatus(0, False)

    def __init__(self, cooco: Iterable[CooCo] | None) -> None:
        if cooco is not None:
            self.__coocos = tuple(cooco)
            self.__is_cooco_set = True
        else:
            self.__coocos = ()
            self.__is_cooco_set = False

    def __getitem__(self, cookie_id: str) -> CooCo:
        for cooco in self.__coocos:
            if cooco.cookie_id == cookie_id:
                return cooco

        message = f"Cookie ID '{cookie_id}' not found"
        raise KeyError(message)

    @staticmethod
    def __get_optional_cookie_groups() -> QuerySet[CookieGroup]:
        return CookieGroup.objects.exclude(is_required=True)  # type: ignore[attr-defined]

    @classmethod
    def from_request(cls, request: HttpRequest) -> Self:
        try:
            cooco_dict = json.loads(request.COOKIES[cls.COOCO_COOKIE_NAME])
        except (KeyError, json.decoder.JSONDecodeError):
            return cls(None)

        _coocos = []

        for cookie_group in cls.__get_optional_cookie_groups():
            cooco_status = cooco_dict.get(cookie_group.cookie_id)

            if (
                not isinstance(cooco_status, Sequence)
                or len(cooco_status) != len(cls.DEFAULT_COOCO_STATUS)
                or not isinstance(cooco_status[0], int)
                or not isinstance(cooco_status[1], bool)
            ):
                cooco_status = cls.DEFAULT_COOCO_STATUS

            _coocos.append(
                CooCo(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cooco_status=CooCoStatus(*cooco_status),
                )
            )

        return cls(_coocos)

    @classmethod
    def parse_cooco_form(cls, cooco_form: dict[str, Any]) -> Self:
        return cls(
            (
                CooCo(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cooco_status=CooCoStatus(
                        cookie_group.version,
                        cooco_form.get(cookie_group.cookie_id) == "on",
                    ),
                )
                for cookie_group in cls.__get_optional_cookie_groups()
            )
        )

    @classmethod
    def all_cookies_accepted(cls) -> Self:
        return cls(
            (
                CooCo(
                    cookie_id=cookie_group.cookie_id,
                    current_version=cookie_group.version,
                    cooco_status=CooCoStatus(cookie_group.version, True),
                )
                for cookie_group in cls.__get_optional_cookie_groups()
            )
        )

    def set_cooco_cookie(self, response: THttpResponse) -> THttpResponse:
        response.set_cookie(
            self.COOCO_COOKIE_NAME,
            json.dumps({cooco.cookie_id: cooco.cooco_status for cooco in self.__coocos}),
            max_age=self.COOCO_COOKIE_MAX_AGE,
            samesite="Lax",
        )

        return response

    def is_cooco_outdated(self) -> bool:
        return not self.__is_cooco_set or any(cooco.is_version_outdated for cooco in self.__coocos)

    def is_cookie_group_accepted(self, cookie_id: str) -> bool:
        return self.__is_cooco_set and self[cookie_id].is_accepted
