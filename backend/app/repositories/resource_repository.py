from sqlalchemy.orm import Session

from backend.app.models.resource import Resource
from backend.app.schemas.resource import ResourceCreate, ResourceUpdate


def create_resource(db: Session, resource: ResourceCreate) -> Resource:
    db_resource = Resource(
        name=resource.name,
        resource_type=resource.resource_type,
        cpu_cores=resource.cpu_cores,
        memory_gb=resource.memory_gb,
        storage_gb=resource.storage_gb,
        status="running",
    )

    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)

    return db_resource


def get_resources(db: Session) -> list[Resource]:
    return db.query(Resource).all()


def get_resource(db: Session, resource_id: int) -> Resource | None:
    return db.query(Resource).filter(Resource.id == resource_id).first()


def update_resource(
    db: Session,
    resource: Resource,
    updates: ResourceUpdate,
) -> Resource:

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)

    return resource


def delete_resource(db: Session, resource: Resource) -> None:
    db.delete(resource)
    db.commit()