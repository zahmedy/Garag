from pydantic import BaseModel

class PresignRequest(BaseModel):
    filename: str
    content_type: str

class PresignResponse(BaseModel):
    upload_url: str
    storage_key: str
    public_url: str

class MediaCompleteRequest(BaseModel):
    storage_key: str
    public_url: str