from http import HTTPStatus

import pytest
from pydantic.error_wrappers import ValidationError
from example.app.views.error import ErrorModel, ErrorResponse


class TestErrorModel:

    @pytest.mark.parametrize(
        "code, message, details",
        [
            (400, "test msg", None),
            ("500", "test msg", [{}]),
            (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
            (404, "test msg", [{"key": {"foo": "bar"}, "key2": [1, 2, 3]}]),
            ("401", "test msg", None),
        ],
    )
    def test_should_create_error_model(self, code, message, details):
        # given / when
        error = ErrorModel(code=code, message=message, details=details)

        # then
        assert error.code == int(code)
        assert error.message == message
        assert error.status == HTTPStatus(int(code)).name
        assert error.details == details
        schema = error.schema()
        assert schema["description"] == "Error model."
        assert schema["properties"]["status"] == {
            "title": "Status",
            "type": "string",
        }
        assert "status" in schema["required"]

    @pytest.mark.parametrize(
        "code, message, details",
        [
            (500, {}, [{}]),
            (403, "test msg", "foobar"),
            (None, None, 123),
            ({}, [], None),
            (False, "test msg", None),
        ],
    )
    def test_should_raise_when_invalid_arguments(self, code, message, details):
        # given / when / then
        with pytest.raises(ValidationError):
            ErrorModel(code=code, message=message, details=details)


class TestErrorResponse:

    @pytest.mark.parametrize(
        "code, message, details",
        [
            (400, "test msg", None),
            ("500", "test msg", [{}]),
            (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
            (404, "test msg", [{"key": {"foo": "bar"}, "key2": [1, 2, 3]}]),
            ("401", "test msg", None),
        ],
    )
    def test_should_create_error_response(self, code, message, details):
        # given / when
        response = ErrorResponse(code=code, message=message, details=details)

        # then
        assert response.error.code == int(code)
        assert response.error.message == message
        assert response.error.status == HTTPStatus(int(code)).name
        assert response.error.details == details
        schema = response.schema()
        assert schema["description"] == "Error response model."

    @pytest.mark.parametrize(
        "code, message, details",
        [
            (500, {}, [{}]),
            (403, "test msg", "foobar"),
            (None, None, 123),
            ({}, [], None),
            (False, "test msg", None),
        ],
    )
    def test_should_raise_when_invalid_arguments(self, code, message, details):
        # given / when / then
        with pytest.raises(ValidationError):
            ErrorResponse(code=code, message=message, details=details)
