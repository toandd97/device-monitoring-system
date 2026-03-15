from typing import Any, Dict, List, Optional

from src.common.utils import utc_now_iso
from src.database.mongo_connection import MongoConnection


class BaseModel:
    collection_name: str

    @classmethod
    def _collection(cls):
        return MongoConnection.get_collection(cls.collection_name)

    @classmethod
    def insert_one(cls, document: Dict[str, Any]) -> str:
        if document is None:
            document = {}
            
        if not document.get("created_time"):
            document["created_time"] = utc_now_iso()
        if not document.get("updated_time"):
            document["updated_time"] = document["created_time"]
            
        result = cls._collection().insert_one(document)
        return str(result.inserted_id)

    @classmethod
    def find_one(cls, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return cls._collection().find_one(query)

    @classmethod
    def find_all(cls, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        query = query or {}
        return list(cls._collection().find(query))

    @classmethod
    def find_with_fields(
        cls,
        query: Dict[str, Any],
        fields: Dict[str, int],
    ) -> List[Dict[str, Any]]:
        return list(cls._collection().find(query, fields))

    @classmethod
    def update_one(
        cls,
        query: Dict[str, Any],
        update: Dict[str, Any],
    ) -> int:
        if update is None:
            update = {}
            
        target_set = update.get("$set") or {}
        target_set["updated_time"] = utc_now_iso()
        update["$set"] = target_set
        
        result = cls._collection().update_one(query, update)
        return result.modified_count

    @classmethod
    def delete_one(cls, query: Dict[str, Any]) -> int:
        result = cls._collection().delete_one(query)
        return result.deleted_count

