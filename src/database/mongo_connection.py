from typing import Any

from pymongo import MongoClient

from config.mongo_config import get_mongo_config
from src.common.logger import get_logger


logger = get_logger(__name__)


class MongoConnection:
    _client: MongoClient | None = None

    @classmethod
    def connect(cls) -> MongoClient:
        if cls._client is None:
            cfg = get_mongo_config()
            logger.info("Connecting to MongoDB %s", cfg["uri"])
            cls._client = MongoClient(cfg["uri"])
        return cls._client

    @classmethod
    def get_database(cls):
        client = cls.connect()
        cfg = get_mongo_config()
        return client[cfg["db_name"]]

    @classmethod
    def get_collection(cls, name: str):
        db = cls.get_database()
        return db[name]

    @classmethod
    def close(cls) -> None:
        if cls._client is not None:
            logger.info("Closing MongoDB connection")
            cls._client.close()
            cls._client = None

