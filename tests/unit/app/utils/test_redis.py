from unittest import mock
from asyncio import Future

import pytest
from redis import asyncio as aioredis
from example.app.utils import RedisClient
from example.config import redis as redis_conf


class TestRedisClient:

    @pytest.fixture
    def async_mock(self):
        yield mock.MagicMock(return_value=Future())

    def test_should_create_client_and_populate_defaults(self):
        # given / when
        RedisClient.open_redis_client()

        # then
        client = RedisClient.redis_client
        assert isinstance(client, aioredis.Redis)
        connection_kwargs = client.connection_pool.connection_kwargs
        assert connection_kwargs["port"] == redis_conf.REDIS_PORT
        assert connection_kwargs["host"] == redis_conf.REDIS_HOST

    def test_should_create_client_with_auth(self):
        # given
        redis_conf.REDIS_USERNAME = "John"
        redis_conf.REDIS_PASSWORD = "Secret"

        # when
        RedisClient.redis_client = None
        RedisClient.open_redis_client()

        # then
        client = RedisClient.redis_client
        assert isinstance(client, aioredis.Redis)
        connection_kwargs = client.connection_pool.connection_kwargs
        assert connection_kwargs["username"] == "John"
        assert connection_kwargs["password"] == "Secret"

    def test_should_create_sentinel_client(self):
        # given
        redis_conf.REDIS_USE_SENTINEL = True

        # when
        RedisClient.redis_client = None
        RedisClient.open_redis_client()

        # then
        client = RedisClient.redis_client
        assert isinstance(client, aioredis.Redis)
        assert client.connection_pool.service_name == "mymaster"

    @pytest.mark.asyncio
    async def test_should_execute_ping_and_return_true(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.ping = async_mock
        async_mock.return_value.set_result(True)

        # when
        result = await RedisClient.ping()

        # then
        assert result
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_ping_and_return_false(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.ping = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        result = await RedisClient.ping()

        # then
        assert not result
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_set_and_return_response(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.set = async_mock
        async_mock.return_value.set_result("OK")

        # when
        result = await RedisClient.set("key", "value")

        # then
        assert result == "OK"
        async_mock.assert_called_once_with("key", "value")

    @pytest.mark.asyncio
    async def test_should_execute_set_and_raise(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.set = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        # when / then
        with pytest.raises(aioredis.RedisError):
            await RedisClient.set("key", "value")

    @pytest.mark.asyncio
    async def test_should_execute_rpush_and_return_response(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.rpush = async_mock
        async_mock.return_value.set_result(10)

        # when
        result = await RedisClient.rpush("key", "value")

        # then
        assert result == 10
        async_mock.assert_called_once_with("key", "value")

    @pytest.mark.asyncio
    async def test_should_execute_rpush_and_raise(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.rpush = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        # when / then
        with pytest.raises(aioredis.RedisError):
            await RedisClient.rpush("key", "value")

    @pytest.mark.asyncio
    async def test_should_execute_exists_and_return_response(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.exists = async_mock
        async_mock.return_value.set_result(True)

        # when
        result = await RedisClient.exists("key")

        # then
        assert result
        async_mock.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_should_execute_exists_and_raise(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.exists = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        # when / then
        with pytest.raises(aioredis.RedisError):
            await RedisClient.exists("key")

    @pytest.mark.asyncio
    async def test_should_execute_get_and_return_response(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.get = async_mock
        async_mock.return_value.set_result("value")

        # when
        result = await RedisClient.get("key")

        # then
        assert result == "value"
        async_mock.assert_called_once_with("key")

    @pytest.mark.asyncio
    async def test_should_execute_get_and_raise(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.get = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        # when / then
        with pytest.raises(aioredis.RedisError):
            await RedisClient.get("key")

    @pytest.mark.asyncio
    async def test_should_execute_lrange_and_return_response(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.lrange = async_mock
        async_mock.return_value.set_result(["value", "value2"])

        # when
        result = await RedisClient.lrange("key", 1, -1)

        # then
        assert result == ["value", "value2"]
        async_mock.assert_called_once_with("key", 1, -1)

    @pytest.mark.asyncio
    async def test_should_execute_lrange_and_raise(self, async_mock):
        # given
        RedisClient.open_redis_client()
        RedisClient.redis_client.lrange = async_mock
        async_mock.side_effect = aioredis.RedisError("Fake error")

        # when / then
        with pytest.raises(aioredis.RedisError):
            await RedisClient.lrange("key", 1, -1)
