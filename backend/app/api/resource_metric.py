from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.resource_metric import (
    ResourceMetricCreate,
    ResourceMetricResponse,
)
from backend.app.services.resource_metric import (
    create_metric as create_metric_service,
    get_metrics as get_metrics_service,
    get_latest_metric as get_latest_metric_service,
)
from backend.app.services.resource_service import get_resource as get_resource_service


router = APIRouter(
    prefix="/resources/{resource_id}/metrics",
    tags=["Resource Metrics"],
)


@router.post("/", response_model=ResourceMetricResponse)
def create_metric(
    resource_id: int,
    metric: ResourceMetricCreate,
    db: Session = Depends(get_db),
):
    resource = get_resource_service(db, resource_id)

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    return create_metric_service(
        db,
        resource_id,
        metric,
    )


@router.get("/", response_model=list[ResourceMetricResponse])
def get_metrics(
    resource_id: int,
    db: Session = Depends(get_db),
):
    resource = get_resource_service(db, resource_id)

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    return get_metrics_service(
        db,
        resource_id,
    )


@router.get("/latest", response_model=ResourceMetricResponse)
def get_latest_metric(
    resource_id: int,
    db: Session = Depends(get_db),
):
    resource = get_resource_service(db, resource_id)

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    metric = get_latest_metric_service(
        db,
        resource_id,
    )

    if metric is None:
        raise HTTPException(
            status_code=404,
            detail="No metrics found for this resource",
        )

    return metric