from typing import Dict, Any

from config.settings import settings


def get_mongo_config() -> Dict[str, Any]:
    return {
        "uri": str(settings.mongo_uri),
        "db_name": settings.mongo_db_name,
    }

