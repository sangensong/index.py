import sys
import typing

import pytest

from indexpy.openapi.functions import (
    GenericType,
    describe_response,
    describe_responses,
    merge_openapi_info,
)


@pytest.mark.parametrize(
    "instance,boolean",
    [
        (typing.List[str], True),
        (typing.Union[str, bytes], True),
        (typing.Tuple[str, str], True),
        (typing.Dict[str, str], True),
        (str, False),
        (int, False),
        (float, False),
    ],
)
def test_generic_type(instance, boolean):
    assert isinstance(instance, GenericType) == boolean


@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason="https://www.python.org/dev/peps/pep-0585/",
)
def test_pep585():
    assert isinstance(list[str], GenericType)
    assert isinstance(dict[str, str], GenericType)
    assert isinstance(tuple[str, str], GenericType)
    assert not isinstance(str, GenericType)
    assert not isinstance(bytes, GenericType)
    assert not isinstance(float, GenericType)


def test_describe_response():
    class HTTP:
        @describe_response(200, "ok")
        @describe_response(400, "bad request")
        async def get(self):
            pass

    assert HTTP.get.__responses__ == {
        200: {"description": "ok"},
        400: {"description": "bad request"},
    }


def test_describe_responses():
    class HTTP:
        @describe_responses(
            {
                200: {"description": "ok"},
                400: {"description": "bad request"},
            }
        )
        async def get(self):
            pass

    assert HTTP.get.__responses__ == {
        200: {"description": "ok"},
        400: {"description": "bad request"},
    }


@pytest.mark.parametrize(
    "f,s,r",
    [
        ({"a": 1}, {"b": 1}, {"a": 1, "b": 1}),
        ({"a": {"a": 1}, "b": 1}, {"a": {"b": 1}}, {"a": {"a": 1, "b": 1}, "b": 1}),
        ({"a": (1, 2)}, {"a": (3,)}, {"a": [1, 2, 3]}),
    ],
)
def test_merge_openapi_info(f, s, r):
    assert merge_openapi_info(f, s) == r
