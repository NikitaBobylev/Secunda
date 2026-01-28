import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from app.models.activity import Activity
from app.models.organization import Organization

logger = logging.getLogger(__name__)


class OrganizationRepository:
    @staticmethod
    def _base_query() -> Select:
        return select(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.phones),
            joinedload(Organization.activities),
        )

    async def get_by_id(self, db: AsyncSession, organization_id: int) -> Organization | None:
        result = await db.execute(
            self._base_query().where(
                Organization.id == organization_id
            )
        )
        return result.unique().scalars().first()

    @staticmethod
    def list_by_building(building_id: int, query: Select) -> Select:
        return query.where(Organization.building_id == building_id)

    @staticmethod
    def list_by_activity(
        query: Select,
        activity_ids: list[int],
    ) -> Select:

        query = (
            query.join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .distinct()
        )
        return query

    async def search(
        self,
        db: AsyncSession,
        name: str | None,
        activity_ids: list[int] | None,
        building_id: int | None,
        offset: int,
        limit: int,
    ) -> tuple[list[Organization], int]:
        query = self._base_query()

        if activity_ids:
            query = self.list_by_activity(query=query, activity_ids=activity_ids)

        if building_id is not None:
            query = self.list_by_building(query=query, building_id=building_id)

        if name is not None:
            pattern = f"%{name}%"
            query = query.filter(Organization.name.ilike(pattern))

        total = await db.scalar(
            select(func.count()).select_from(query.subquery())
        )
        ofseted = await db.execute(query.offset(offset).limit(limit).order_by(Organization.id))
        return ofseted.unique().scalars().all(), int(total or 0)

    async def list_by_building_ids(
        self, db: AsyncSession, building_ids: list[int], offset: int, limit: int
    ) -> tuple[list[Organization], int]:
        if not building_ids:
            return [], 0
        total = await db.scalar(
            select(func.count()).select_from(
                select(Organization.id)
                .where(Organization.building_id.in_(building_ids))
                .subquery()
            )
        )
        result = await db.execute(
            self._base_query()
            .where(Organization.building_id.in_(building_ids))
            .offset(offset)
            .limit(limit)
        )
        return result.unique().scalars().all(), int(total or 0)
