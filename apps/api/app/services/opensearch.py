from opensearchpy import OpenSearch
from app.core.config import settings

def os_client() -> OpenSearch:
    return OpenSearch(hosts=[settings.OPENSEARCH_URL])

def ensure_index():
    c = os_client()
    index = settings.OPENSEARCH_INDEX
    if c.indices.exists(index=index):
        return
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "status": {"type": "keyword"},
                "city": {"type": "keyword"},
                "district": {"type": "keyword"},
                "make_id": {"type": "integer"},
                "model_id": {"type": "integer"},
                "year": {"type": "integer"},
                "price_sar": {"type": "integer"},
                "mileage_km": {"type": "integer"},
                "body_type": {"type": "keyword"},
                "transmission": {"type": "keyword"},
                "fuel_type": {"type": "keyword"},
                "drivetrain": {"type": "keyword"},
                "condition": {"type": "keyword"},
                "title_ar": {"type": "text"},
                "description_ar": {"type": "text"},
                "published_at": {"type": "date"},
            }
        }
    }
    c.indices.create(index=index, body=mapping)