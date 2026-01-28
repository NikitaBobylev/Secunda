from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    activities: Mapped[list["Activity"]] = relationship(
        secondary=organization_activities,
        back_populates="organizations",
    )


if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.building import Building
    from app.models.phone import OrganizationPhone
