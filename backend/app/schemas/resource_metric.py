from datetime import datetime

from pydantic import BaseModel, Field


class ResourceMetricCreate(BaseModel):
    cpu_usage_percent: float = Field(ge=0, le=100)
    memory_usage_percent: float = Field(ge=0, le=100)
    storage_usage_percent: float = Field(ge=0, le=100)


class ResourceMetricResponse(ResourceMetricCreate):
    id: int
    resource_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True