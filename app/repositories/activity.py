import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity

logger = logging.getLogger(__name__)


class ActivityRepository:
    @staticmethod
    async def list_items(
        db: AsyncSession, offset: int, limit: int
    ) -> tuple[list[Activity], int]:
        total = await db.scalar(select(func.count()).select_from(Activity))
        result = await db.execute(select(Activity).offset(offset).limit(limit))
        return result.scalars().all(), int(total or 0)

    @staticmethod
    async def list_all(db: AsyncSession) -> list[Activity]:
        result = await db.execute(select(Activity))
        return result.scalars().all()
