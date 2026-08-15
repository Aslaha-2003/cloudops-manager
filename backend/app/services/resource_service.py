from sqlalchemy.orm import Session

from backend.app.schemas.resource import ResourceCreate, ResourceUpdate
from backend.app.repositories.resource_repository import (
    create_resource as create_resource_repository,
    get_resources as get_resources_repository,
    get_resource as get_resource_repository,
    update_resource as update_resource_repository,
    delete_resource as delete_resource_repository,
)


def create_resource(db: Session, resource: ResourceCreate):
    return create_resource_repository(db, resource)


def get_resources(db: Session):
    return get_resources_repository(db)


def get_resource(db: Session, resource_id: int):
    return get_resource_repository(db, resource_id)


def update_resource(
    db: Session,
    resource_id: int,
    updates: ResourceUpdate,
):
    resource = get_resource_repository(db, resource_id)

    if resource is None:
        return None

    return update_resource_repository(db, resource, updates)


def delete_resource(db: Session, resource_id: int):
    resource = get_resource_repository(db, resource_id)

    if resource is None:
        return False

    delete_resource_repository(db, resource)
    return True