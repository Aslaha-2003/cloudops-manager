from sqlalchemy.orm import Session

from backend.app.models.resource import Resource
from backend.app.schemas.resource import ResourceCreate


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