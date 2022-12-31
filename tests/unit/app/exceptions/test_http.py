from unittest import mock

import pytest
from starlette.requests import Request
from example.app.exceptions import (
    HTTPException,
    http_exception_handler,
)


class TestHttpException:

    @pytest.mark.parametrize(
        "status_code, content, headers",
        [
            (400, "test msg", None),
            (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
            (
                    404,
                    {"key": 123, "key2": 123.123, "foo": "bar"},
                    {"key": {"foo": "bar"}, "key2": [1, 2, 3]},
            ),
        ],
    )
    def test_should_create_exception(self, status_code, content, headers):
        # given / when
        ex = HTTPException(
            status_code=status_code,
            content=content,
            headers=headers,
        )

        # then
        assert issubclass(type(ex), Exception)
        assert ex.status_code == status_code
        assert ex.content == content
        assert ex.headers == headers

    def test_should_create_exception_from_repr_eval(self):
        # given
        ex = HTTPException(
            status_code=200,
            content="OK",
            headers=None,
        )

        # when
        ex_eval = eval(repr(ex))

        # then
        assert ex_eval.status_code == ex.status_code
        assert ex_eval.content == ex.content
        assert ex_eval.headers == ex.headers
        assert isinstance(ex_eval, HTTPException)


class TestHttpExceptionHandler:

    @pytest.fixture
    def fastapi_request(self):
        yield mock.Mock(spec=Request)

    @pytest.mark.asyncio
    async def test_should_return_json_response(self, fastapi_request):
        # given
        ex = HTTPException(
            status_code=502,
            content=[{"key": 123, "key2": 123.123, "foo": "bar"}],
            headers={"foo": "bar"},
        )

        # when
        response = await http_exception_handler(fastapi_request, ex)

        # then
        assert response.status_code == 502
        assert response.body == b'[{"key":123,"key2":123.123,"foo":"bar"}]'
        assert response.headers["foo"] == "bar"
