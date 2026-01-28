import logging
import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building
from app.repositories.building import BuildingRepository
from app.schemas.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return 2 * radius_km * math.asin(math.sqrt(a))


class BuildingService:
    def __init__(self, repo: BuildingRepository | None = None) -> None:
        self.repo = repo or BuildingRepository()

    async def list_buildings(
        self, db: AsyncSession, offset: int, limit: int
    ) -> PaginatedResponse:
        items, total = await self.repo.list_items(db, offset, limit)
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def list_in_radius(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_km: float,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.320 * math.cos(math.radians(latitude)) or 1)

        candidates = await self.repo.list_in_box(
            db,
            latitude - lat_delta,
            latitude + lat_delta,
            longitude - lon_delta,
            longitude + lon_delta,
        )
        filtered = [
            building
            for building in candidates
            if _haversine_km(latitude, longitude, building.latitude, building.longitude)
            <= radius_km
        ]
        total = len(filtered)
        items = filtered[offset : offset + limit]
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def list_in_box(
        self,
        db: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        offset: int,
        limit: int,
    ) -> PaginatedResponse:
        items = await self.repo.list_in_box(db, lat_min, lat_max, lon_min, lon_max)
        total = len(items)
        return PaginatedResponse(
            items=items[offset : offset + limit],
            offset=offset,
            limit=limit,
            total=total,
        )