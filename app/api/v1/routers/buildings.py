from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import api_key_auth
from app.db.session import get_db
from app.schemas.building import BuildingOut
from app.schemas.pagination import PaginatedResponse, PaginationParams, pagination_params
from app.services.buildings import BuildingService

router = APIRouter(dependencies=[Depends(api_key_auth)])
service = BuildingService()


@router.get("/", response_model=PaginatedResponse[BuildingOut])
async def list_buildings(
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_buildings(db, pagination.offset, pagination.limit)