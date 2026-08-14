from pydantic import BaseModel, Field


class ResourceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    resource_type: str
    cpu_cores: int = Field(gt=0)
    memory_gb: float = Field(gt=0)
    storage_gb: float = Field(gt=0)


class ResourceResponse(ResourceCreate):
    id: int
    status: str

    class Config:
        from_attributes = True