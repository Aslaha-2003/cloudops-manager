from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.resource_health import ResourceHealthResponse
from backend.app.services.resource_health import get_resource_health


router = APIRouter(
    prefix="/resources",
    tags=["Resource Health"],
)


@router.get(
    "/{resource_id}/health",
    response_model=ResourceHealthResponse,
)
def get_health(
    resource_id: int,
    db: Session = Depends(get_db),
):
    health = get_resource_health(db, resource_id)

    if health is None:
        raise HTTPException(
            status_code=404,
            detail="Resource or metrics not found",
        )

    return health