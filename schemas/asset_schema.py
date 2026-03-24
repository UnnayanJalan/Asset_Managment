from pydantic import BaseModel

class AssetCreate(BaseModel):
    name: str
    type: str