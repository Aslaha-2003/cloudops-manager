from sqlalchemy.orm import Session

from backend.app.models.resource_metric import ResourceMetrics
from backend.app.schemas.resource_metric import ResourceMetricCreate


def create_metric(
    db: Session,
    resource_id: int,
    metric: ResourceMetricCreate,
) -> ResourceMetrics:
    db_metric = ResourceMetrics(
        resource_id=resource_id,
        cpu_usage_percent=metric.cpu_usage_percent,
        memory_usage_percent=metric.memory_usage_percent,
        storage_usage_percent=metric.storage_usage_percent,
    )

    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)

    return db_metric


def get_metrics(
    db: Session,
    resource_id: int,
) -> list[ResourceMetrics]:
    return (
        db.query(ResourceMetrics)
        .filter(ResourceMetrics.resource_id == resource_id)
        .order_by(ResourceMetrics.recorded_at.desc())
        .all()
    )


def get_latest_metric(
    db: Session,
    resource_id: int,
) -> ResourceMetrics | None:
    return (
        db.query(ResourceMetrics)
        .filter(ResourceMetrics.resource_id == resource_id)
        .order_by(ResourceMetrics.recorded_at.desc())
        .first()
    )