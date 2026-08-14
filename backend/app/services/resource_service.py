from sqlalchemy.orm import Session

from backend.app.schemas.resource import ResourceCreate
from backend.app.repositories.resource_repository import (
    create_resource as create_resource_repository,
    get_resources as get_resources_repository,
)


def create_resource(db: Session, resource: ResourceCreate):
    return create_resource_repository(db, resource)


def get_resources(db: Session):
    return get_resources_repository(db)