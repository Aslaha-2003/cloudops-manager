from sqlalchemy.orm import Session

from backend.app.schemas.resource_metric import ResourceMetricCreate
from backend.app.repositories.resource_metric import (
    create_metric as create_metric_repository,
    get_metrics as get_metrics_repository,
    get_latest_metric as get_latest_metric_repository,
)


def create_metric(
    db: Session,
    resource_id: int,
    metric: ResourceMetricCreate,
):
    return create_metric_repository(
        db,
        resource_id,
        metric,
    )


def get_metrics(
    db: Session,
    resource_id: int,
):
    return get_metrics_repository(
        db,
        resource_id,
    )


def get_latest_metric(
    db: Session,
    resource_id: int,
):
    return get_latest_metric_repository(
        db,
        resource_id,
    )