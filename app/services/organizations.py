import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository
from app.schemas.pagination import PaginatedResponse
from app.services.activities import ActivityService
from app.services.buildings import BuildingService

logger = logging.getLogger(__name__)


class OrganizationService:
    def __init__(
        self,
        repo: OrganizationRepository | None = None,
        activity_service: ActivityService | None = None,
        building_service: BuildingService | None = None,
    ) -> None:
        self.repo = repo or OrganizationRepository()
        self.activity_service = activity_service or ActivityService()
        self.building_service = building_service or BuildingService()

    async def get_by_id(
        self, db: AsyncSession, organization_id: int
    ) -> Organization | None:
        return await self.repo.get_by_id(db, organization_id)

    async def list_by_building(
        self, db: AsyncSession, building_id: int, offset: int, limit: int
    ) -> PaginatedResponse:
        items, total = await self.repo.list_by_building(db, building_id, offset, limit)
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def list_by_activity(
        self,
        db: AsyncSession,
        activity_id: int,
        include_descendants: bool,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        activity_ids = [activity_id]
        if include_descendants:
            descendants = await self.activity_service.get_descendant_ids(
                db, activity_id
            )
            if not descendants:
                return PaginatedResponse(items=[], offset=offset, limit=limit, total=0)
            activity_ids = descendants

        items, total = await self.repo.list_by_activity(db, activity_ids, offset, limit)
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def search(
        self,
        db: AsyncSession,
        name: str | None,
        offset: int,
        limit: int,
        building_id: int | None,
        activity_id: int | None,
    ) -> PaginatedResponse:
        activity_ids: list[int] | None = None

        if activity_id is not None:
            activity_ids = [activity_id]

        items, total = await self.repo.search(
            db=db,
            activity_ids=activity_ids,
            building_id=building_id,
            offset=offset,
            limit=limit,
            name=name
        )
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def search_by_activity_name(
        self,
        db: AsyncSession,
        activity_name: str,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        activity_ids = await self.activity_service.get_descendant_ids_by_name(
            db, activity_name
        )
        if not activity_ids:
            return PaginatedResponse(items=[], offset=offset, limit=limit, total=0)

        items, total = await self.repo.search(
            db=db,
            activity_ids=activity_ids,
            building_id=None,
            offset=offset,
            limit=limit,
            name=None,
        )
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def list_within_radius(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        buildings_page = await self.building_service.list_in_radius(
            db, latitude, longitude, radius_km, 0, 10_000
        )
        building_ids = [building.id for building in buildings_page.items]
        items, total = await self.repo.list_by_building_ids(
            db, building_ids, offset, limit
        )
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def list_within_box(
        self,
        db: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        buildings_page = await self.building_service.list_in_box(
            db, lat_min, lat_max, lon_min, lon_max, 0, 10_000
        )
        building_ids = [building.id for building in buildings_page.items]
        items, total = await self.repo.list_by_building_ids(
            db, building_ids, offset, limit
        )
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)
