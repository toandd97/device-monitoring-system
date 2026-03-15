import copy
from src.common.utils import generate_uuid, utc_now_iso
from src.database.base_model import BaseModel


class MetricFields:
    EVENT_ID = "event_id"
    EVENT_TYPE = "event_type"
    TIMESTAMP = "timestamp"
    SOURCE = "source"
    PAYLOAD = "payload"


class MetricStatus:
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class MetricDocument(BaseModel):
    collection_name = "metrics"

    @staticmethod
    def build_document(event: dict, status: str) -> dict:
        if event is None:
            event = {}
            
        doc = copy.deepcopy(event)
        doc["_id"] = doc.get(MetricFields.EVENT_ID) or generate_uuid()
        
        payload = doc.get(MetricFields.PAYLOAD) or {}
        payload["status"] = status
        doc[MetricFields.PAYLOAD] = payload
        
        if not doc.get(MetricFields.TIMESTAMP):
            doc[MetricFields.TIMESTAMP] = utc_now_iso()
            
        return doc

