from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class ResourceMetrics(Base):
    __tablename__ = "resource_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cpu_usage_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    memory_usage_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    storage_usage_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    resource = relationship("Resource")