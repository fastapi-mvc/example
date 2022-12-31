import pytest
import aiohttp
from aioresponses import aioresponses
from example.app.utils import AiohttpClient


class TestAiohttpClient:

    @pytest.fixture
    def fake_web(self):
        with aioresponses() as mock:
            yield mock

    def test_should_create_aiohttp_client(self):
        # given / when
        AiohttpClient.get_aiohttp_client()

        # then
        assert isinstance(AiohttpClient.aiohttp_client, aiohttp.ClientSession)

    @pytest.mark.asyncio
    async def test_should_close_aiohttp_client(self):
        # given
        AiohttpClient.get_aiohttp_client()

        # when
        await AiohttpClient.close_aiohttp_client()

        # then
        assert AiohttpClient.aiohttp_client is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, headers, raise_for_status",
        [
            (200, None, True),
            (201, {"foo": "bar"}, False),
            (404, None, False),
            (500, {"API": "KEY"}, False),
        ],
    )
    async def test_should_execute_get_and_return_response(self, fake_web, status, headers, raise_for_status):
        # given
        fake_web.get(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when
        response = await AiohttpClient.get(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        # then
        assert response.status == status
        assert await response.json() == {"fake": "response"}
        if headers:
            assert response.request_info.headers == headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [404, 500])
    async def test_should_execute_get_and_raise(self, fake_web, status):
        # given
        fake_web.get(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when / then
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.get(
                "http://example.com/api",
                raise_for_status=True,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, data, headers, raise_for_status",
        [
            (200, None, None, True),
            (201, {1: 2}, {"foo": "bar"}, True),
            (404, "payload", None, False),
            (500, None, {"API": "KEY"}, False),
        ],
    )
    async def test_should_execute_post_and_return_response(self, fake_web, status, data, headers, raise_for_status):
        # given
        fake_web.post(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when
        response = await AiohttpClient.post(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        # then
        assert response.status == status
        assert await response.json() == {"fake": "response"}
        if headers:
            assert response.request_info.headers == headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [404, 500])
    async def test_should_execute_post_and_raise(self, fake_web, status):
        # given
        fake_web.post(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when / then
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.post(
                "http://example.com/api",
                raise_for_status=True,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, data, headers, raise_for_status",
        [
            (200, None, None, True),
            (201, {1: 2}, {"foo": "bar"}, True),
            (404, "payload", None, False),
            (500, None, {"API": "KEY"}, False),
        ],
    )
    async def test_should_execute_put_and_return_response(self, fake_web, status, data, headers, raise_for_status):
        # given
        fake_web.put(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when
        response = await AiohttpClient.put(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        # then
        assert response.status == status
        assert await response.json() == {"fake": "response"}
        if headers:
            assert response.request_info.headers == headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [404, 500])
    async def test_should_execute_put_and_raise(self, fake_web, status):
        # given
        fake_web.put(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when / then
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.put(
                "http://example.com/api",
                raise_for_status=True,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, data, headers, raise_for_status",
        [
            (200, None, None, True),
            (201, {1: 2}, {"foo": "bar"}, True),
            (404, "payload", None, False),
            (500, None, {"API": "KEY"}, False),
        ],
    )
    async def test_should_execute_patch_and_return_response(self, fake_web, status, data, headers, raise_for_status):
        # given
        fake_web.patch(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when
        response = await AiohttpClient.patch(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        # then
        assert response.status == status
        assert await response.json() == {"fake": "response"}
        if headers:
            assert response.request_info.headers == headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [404, 500])
    async def test_should_execute_patch_and_raise(self, fake_web, status):
        # given
        fake_web.patch(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when / then
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.patch(
                "http://example.com/api",
                raise_for_status=True,
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, headers, raise_for_status",
        [
            (200, None, True),
            (201, {"foo": "bar"}, False),
            (404, None, False),
            (500, {"API": "KEY"}, False),
        ],
    )
    async def test_should_execute_delete_and_return_response(self, fake_web, status, headers, raise_for_status):
        # given
        fake_web.delete(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when
        response = await AiohttpClient.delete(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        # then
        assert response.status == status
        assert await response.json() == {"fake": "response"}
        if headers:
            assert response.request_info.headers == headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [404, 500])
    async def test_should_execute_delete_and_raise(self, fake_web, status):
        # given
        fake_web.delete(
            "http://example.com/api",
            status=status,
            payload={"fake": "response"},
        )
        AiohttpClient.get_aiohttp_client()

        # when / then
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.delete(
                "http://example.com/api",
                raise_for_status=True,
            )
