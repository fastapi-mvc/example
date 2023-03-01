"""Redis client class utility."""
from typing import TypeVar, Dict, Union, List, AnyStr
import logging

from redis import asyncio as aioredis
from example.config import redis as redis_conf


R = TypeVar("R")


class RedisClient(object):
    """Define Redis utility.

    Utility class for handling Redis database connection and operations.

    Attributes:
        redis_client (aioredis.Redis, optional): Redis client object instance.
        log (logging.Logger): Logging handler for this class.
        base_redis_init_kwargs (typing.Dict[str, typing.Union[str, int]]): Common
            kwargs regardless other Redis configuration
        connection_kwargs (typing.Optional[typing.Dict[str, str]]): Extra kwargs
            for Redis object init.

    """

    redis_client: aioredis.Redis = None
    log: logging.Logger = logging.getLogger(__name__)
    base_redis_init_kwargs: Dict[str, Union[str, int]] = {
        "encoding": "utf-8",
        "port": redis_conf.REDIS_PORT,
    }
    connection_kwargs: Dict[str, str] = {}

    @classmethod
    def open_redis_client(cls) -> aioredis.Redis:
        """Create Redis client session object instance.

        Based on configuration create either Redis client or Redis Sentinel.

        Returns:
            aioredis.Redis: Redis object instance.

        """
        if cls.redis_client is None:
            cls.log.debug("Initialize Redis client.")
            if redis_conf.REDIS_USERNAME and redis_conf.REDIS_PASSWORD:
                cls.connection_kwargs = {
                    "username": redis_conf.REDIS_USERNAME,
                    "password": redis_conf.REDIS_PASSWORD,
                }

            if redis_conf.REDIS_USE_SENTINEL:
                sentinel = aioredis.sentinel.Sentinel(
                    [(redis_conf.REDIS_HOST, redis_conf.REDIS_PORT)],
                    sentinel_kwargs=cls.connection_kwargs,
                )
                cls.redis_client = sentinel.master_for("mymaster")
            else:
                cls.base_redis_init_kwargs.update(cls.connection_kwargs)
                cls.redis_client = aioredis.from_url(
                    f"redis://{redis_conf.REDIS_HOST}",
                    **cls.base_redis_init_kwargs,
                )

        return cls.redis_client

    @classmethod
    async def close_redis_client(cls) -> None:
        """Close Redis client."""
        if cls.redis_client:
            cls.log.debug("Closing Redis client")
            await cls.redis_client.close()

    @classmethod
    async def ping(cls) -> bool:
        """Execute Redis PING command.

        Ping the Redis server.

        Returns:
            bool: Boolean, whether Redis client could ping Redis server.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        # Note: Not sure if this shouldn't be deep copy instead?
        redis_client = cls.redis_client

        cls.log.debug("Execute Redis PING command")
        try:
            return await redis_client.ping()
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis PING command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            return False

    @classmethod
    async def set(cls, key, value) -> R:
        """Execute Redis SET command.

        Set key to hold the string value. If key already holds a value, it is
        overwritten, regardless of its type.

        Args:
            key (str): Redis db key.
            value (str): Value to be set.

        Returns:
            response: Redis SET command response, for more info
                look: https://redis.io/commands/set#return-value

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(f"Execute Redis SET command, key: {key}, value: {value}")
        try:
            return await redis_client.set(key, value)
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis SET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def rpush(cls, key: str, value: Union[str, List[AnyStr]]) -> int:
        """Execute Redis RPUSH command.

        Insert all the specified values at the tail of the list stored at key.
        If key does not exist, it is created as empty list before performing
        the push operation. When key holds a value that is not a list, an
        error is returned.

        Args:
            key (str): Redis db key.
            value (typing.Union[str, List[typing.AnyStr]]): Single or multiple
                values to append.

        Returns:
            int: Length of the list after the push operation.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(
            f"Execute Redis RPUSH command, key: {key}, value: {value}"
        )
        try:
            return await redis_client.rpush(key, value)
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis RPUSH command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def exists(cls, key: str) -> bool:
        """Execute Redis EXISTS command.

        Returns if key exists.

        Args:
            key (str): Redis db key.

        Returns:
            bool: Boolean whether key exists in Redis db.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(f"Execute Redis EXISTS command, key: {key}")
        try:
            return await redis_client.exists(key)
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis EXISTS command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def get(cls, key: str) -> str:
        """Execute Redis GET command.

        Get the value of key. If the key does not exist the special value None
        is returned. An error is returned if the value stored at key is not a
        string, because GET only handles string values.

        Args:
            key (str): Redis db key.

        Returns:
            str: Value of key.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(f"Execute Redis GET command, key: {key}")
        try:
            return await redis_client.get(key)
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis GET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def lrange(cls, key: str, start: int, end: int) -> str:
        """Execute Redis LRANGE command.

        Returns the specified elements of the list stored at key. The offsets
        start and stop are zero-based indexes, with 0 being the first element
        of the list (the head of the list), 1 being the next element and so on.
        These offsets can also be negative numbers indicating offsets starting
        at the end of the list. For example, -1 is the last element of the
        list, -2 the penultimate, and so on.

        Args:
            key (str): Redis db key.
            start (int): Start offset value.
            end (int): End offset value.

        Returns:
            str: Returns the specified elements of the list stored at key.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client
        cls.log.debug(
            f"Execute Redis LRANGE command, "
            f"key: {key}, start: {start}, end: {end}"
        )
        try:
            return await redis_client.lrange(key, start, end)
        except aioredis.RedisError as ex:
            cls.log.exception(
                "Redis LRANGE command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex
