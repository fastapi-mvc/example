import pytest
from pydantic.error_wrappers import ValidationError
from example.app.views import ReadyResponse


class TestReadyResponse:

    @pytest.mark.parametrize(
        "value",
        [
            "ok",
            "Another string",
            "ąŻŹÐĄŁĘ®ŒĘŚÐ",
            15,
            False,
        ],
    )
    def test_should_create_ready_response(self, value):
        # given / when
        ready = ReadyResponse(status=value)

        # then
        assert ready.status == str(value)
        schema = ready.schema()
        assert schema["description"] == "Ready response model."

    @pytest.mark.parametrize(
        "value",
        [
            ({"status": "ok"}),
            ([123, "ok"]),
            (["ok", "ready"]),
        ],
    )
    def test_should_raise_when_invalid_argument(self, value):
        # given / when / then
        with pytest.raises(ValidationError):
            ReadyResponse(status=value)
