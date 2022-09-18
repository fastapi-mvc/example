"""Application implementation - utilities.

Resources:
    1. https://aioredis.readthedocs.io/en/latest/

"""
from example.app.utils.aiohttp_client import AiohttpClient
from example.app.utils.redis import RedisClient


__all__ = ("AiohttpClient", "RedisClient")
