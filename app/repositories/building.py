import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building

logger = logging.getLogger(__name__)


class BuildingRepository:
    @staticmethod
    async def list_items(
        db: AsyncSession, offset: int, limit: int
    ) -> tuple[list[Building], int]:
        total = await db.scalar(select(func.count()).select_from(Building))
        result = await db.execute(select(Building).offset(offset).limit(limit))
        buildings = result.scalars().all()
        return buildings, int(total or 0)

    @staticmethod
    async def list_in_box(
        db: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> list[Building]:
        result = await db.execute(
            select(Building)
            .where(Building.latitude.between(lat_min, lat_max))
            .where(Building.longitude.between(lon_min, lon_max))
        )
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, building: Building) -> Building:
        db.add(building)
        await db.commit()
        await db.refresh(building)
        logger.info("Created building id=%s", building.id)
        return building
