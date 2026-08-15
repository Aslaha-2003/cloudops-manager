from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from backend.app.services.resource_service import (
    create_resource as create_resource_service,
    get_resources as get_resources_service,
    get_resource as get_resource_service,
    update_resource as update_resource_service,
    delete_resource as delete_resource_service,
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


@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
):
    resource = get_resource_service(db, resource_id)

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    updates: ResourceUpdate,
    db: Session = Depends(get_db),
):
    resource = update_resource_service(
        db,
        resource_id,
        updates,
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    return resource


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    deleted = delete_resource_service(db, resource_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    return {
        "message": "Resource deleted successfully"
    }