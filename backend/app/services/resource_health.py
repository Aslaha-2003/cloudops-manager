from sqlalchemy.orm import Session

from backend.app.repositories.resource_metric import get_latest_metric
from backend.app.repositories.resource_repository import get_resource
from backend.app.schemas.resource_health import ResourceHealthResponse


def get_resource_health(
    db: Session,
    resource_id: int,
) -> ResourceHealthResponse | None:
    resource = get_resource(db, resource_id)

    if resource is None:
        return None

    metric = get_latest_metric(db, resource_id)

    if metric is None:
        return None

    usage_values = [
        metric.cpu_usage_percent,
        metric.memory_usage_percent,
        metric.storage_usage_percent,
    ]

    maximum_usage = max(usage_values)

    if maximum_usage >= 90:
        health = "critical"
    elif maximum_usage >= 70:
        health = "warning"
    else:
        health = "healthy"

    return ResourceHealthResponse(
        resource_id=resource.id,
        resource_name=resource.name,
        resource_status=resource.status,
        health=health,
        cpu_usage_percent=metric.cpu_usage_percent,
        memory_usage_percent=metric.memory_usage_percent,
        storage_usage_percent=metric.storage_usage_percent,
    )