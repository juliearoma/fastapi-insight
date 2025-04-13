from typing import List
import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

from src.app.core.helper.etcd_service import EtcdService

etcd_service = EtcdService()
 
class AppSettings(BaseSettings):
    APP_NAME: str = etcd_service.get("APP_NAME", default="FastAPI app")
    APP_DESCRIPTION: str | None = etcd_service.get("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = etcd_service.get("APP_VERSION", default=None)
    LICENSE_NAME: str | None = etcd_service.get("LICENSE", default=None)
    CONTACT_NAME: str | None = etcd_service.get("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = etcd_service.get("CONTACT_EMAIL", default=None)


class CryptSettings(BaseSettings):
    SECRET_KEY: str = etcd_service.get("Crypt:SecretKey", default="default-secret-key")
    ALGORITHM: str = etcd_service.get("Crypt:Algorithm", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = etcd_service.get("Crypt:AccessTokenExpireMinutes", default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = etcd_service.get("Crypt:RefreshTokenExpireDays", default=7)



class DatabaseSettings(BaseSettings):
    pass


class SQLiteSettings(DatabaseSettings):
    SQLITE_URI: str = etcd_service.get("SQLITE_URI", default="./sql_app.db")
    SQLITE_SYNC_PREFIX: str = etcd_service.get("SQLITE_SYNC_PREFIX", default="sqlite:///")
    SQLITE_ASYNC_PREFIX: str = etcd_service.get("SQLITE_ASYNC_PREFIX", default="sqlite+aiosqlite:///")


class MySQLSettings(DatabaseSettings):
    MYSQL_USER: str = etcd_service.get("MYSQL_USER", default="myuser")
    MYSQL_PASSWORD: str = etcd_service.get("MYSQL_PASSWORD", default="mypassword")
    MYSQL_SERVER: str = etcd_service.get("MYSQL_SERVER", default="localhost")
    MYSQL_PORT: int = etcd_service.get("MYSQL_PORT", default=5432)
    MYSQL_DB: str = etcd_service.get("MYSQL_DB", default="dbname")
    #MYSQL_URI: str = f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    MYSQL_URI: str = etcd_service.get("ConnectionStrings:MySqlDb", default="root:whqotn3170@localhost:3306/test")
    MYSQL_SYNC_PREFIX: str = etcd_service.get("MYSQL_SYNC_PREFIX", default="mysql://")
    MYSQL_ASYNC_PREFIX: str = etcd_service.get("MYSQL_ASYNC_PREFIX", default="mysql+aiomysql://")
    MYSQL_URL: str | None = etcd_service.get("MYSQL_URL", default=None)


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = etcd_service.get("POSTGRES_USER", default="myuser")
    POSTGRES_PASSWORD: str = etcd_service.get("POSTGRES_PASSWORD", default="mypassword")
    POSTGRES_SERVER: str = etcd_service.get("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = etcd_service.get("POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = etcd_service.get("POSTGRES_DB", default="postgres")
    POSTGRES_SYNC_PREFIX: str = etcd_service.get("POSTGRES_SYNC_PREFIX", default="postgresql://")
    POSTGRES_ASYNC_PREFIX: str = etcd_service.get("POSTGRES_ASYNC_PREFIX", default="postgresql+asyncpg://")
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL: str | None = etcd_service.get("POSTGRES_URL", default=None)

class LoggingSettings(BaseSettings):
    LOGGING_URI: str = etcd_service.get("Logging:MysqlDb", default="")


class FirstUserSettings(BaseSettings):
    ADMIN_NAME: str = etcd_service.get("ADMIN_NAME", default="admin")
    ADMIN_EMAIL: str = etcd_service.get("ADMIN_EMAIL", default="admin@admin.com")
    ADMIN_USERNAME: str = etcd_service.get("ADMIN_USERNAME", default="admin")
    ADMIN_PASSWORD: str = etcd_service.get("ADMIN_PASSWORD", default="!Ch4ng3Th1sP4ssW0rd!")


class TestSettings(BaseSettings):
    ...


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = etcd_service.get("Redis:Cache:Host", default="localhost")
    REDIS_CACHE_PORT: int = etcd_service.get("Redis:Cache:Port", default=6379)
    REDIS_CACHE_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"


class ClientSideCacheSettings(BaseSettings):
    CLIENT_CACHE_MAX_AGE: int = etcd_service.get("CLIENT_CACHE_MAX_AGE", default=60)


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = etcd_service.get("Redis:Queue:Host", default="localhost")
    REDIS_QUEUE_PORT: int = etcd_service.get("Redis:Queue:Port", default=6379)


class RedisRateLimiterSettings(BaseSettings):
    REDIS_RATE_LIMIT_HOST: str = etcd_service.get("Redis:Late_Limit:Host", default="localhost")
    REDIS_RATE_LIMIT_PORT: int = etcd_service.get("Redis:Late_Limit:Port", default=6379)
    REDIS_RATE_LIMIT_URL: str = f"redis://{REDIS_RATE_LIMIT_HOST}:{REDIS_RATE_LIMIT_PORT}"


class DefaultRateLimitSettings(BaseSettings):
    DEFAULT_RATE_LIMIT_LIMIT: int = etcd_service.get("DEFAULT_RATE_LIMIT_LIMIT", default=10)
    DEFAULT_RATE_LIMIT_PERIOD: int = etcd_service.get("DEFAULT_RATE_LIMIT_PERIOD", default=3600)

class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: str = os.getenv("PYTHON_ENV", "development")

class CorsSettings():
    ALLOW_ORIGINS = etcd_service.get("Cors:Allow_Origins", default="*")



class Settings(
    AppSettings,
    MySQLSettings, 
    PostgresSettings,
    CryptSettings,
    FirstUserSettings,
    TestSettings,
    RedisCacheSettings,
    ClientSideCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
    DefaultRateLimitSettings,
    EnvironmentSettings,
    CorsSettings,
):
    pass


settings = Settings()
