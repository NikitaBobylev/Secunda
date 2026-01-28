from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="ck_activity_level"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    level: Mapped[int]
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id"),
        nullable=True,
    )

    parent: Mapped[Optional["Activity"]] = relationship(
        remote_side="Activity.id",
        back_populates="children",
    )
    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    organizations: Mapped[list["Organization"]] = relationship(
        secondary="organization_activities",
        back_populates="activities",
    )


if TYPE_CHECKING:
    from app.models.organization import Organization
