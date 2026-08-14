from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.resource import ResourceCreate, ResourceResponse
from backend.app.services.resource_service import (
    create_resource as create_resource_service,
    get_resources as get_resources_service,
)

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


@router.get("/", response_model=list[ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return get_resources_service(db)


@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
):
    return create_resource_service(db, resource)