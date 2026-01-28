from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    latitude: Mapped[float]
    longitude: Mapped[float]

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="building",
        cascade="all, delete-orphan",
    )


if TYPE_CHECKING:
    from app.models.organization import Organization
