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


class ResourceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    resource_type: str | None = None
    cpu_cores: int | None = Field(default=None, gt=0)
    memory_gb: float | None = Field(default=None, gt=0)
    storage_gb: float | None = Field(default=None, gt=0)
    status: str | None = None