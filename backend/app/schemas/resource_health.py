from pydantic import BaseModel


class ResourceHealthResponse(BaseModel):
    resource_id: int
    resource_name: str
    resource_status: str
    health: str
    cpu_usage_percent: float
    memory_usage_percent: float
    storage_usage_percent: float