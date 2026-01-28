from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import api_key_auth
from app.db.session import get_db
from app.schemas.activity import ActivityOut
from app.schemas.pagination import PaginatedResponse, PaginationParams, pagination_params
from app.services.activities import ActivityService

router = APIRouter(dependencies=[Depends(api_key_auth)])
service = ActivityService()


@router.get("/", response_model=PaginatedResponse[ActivityOut])
async def list_activities(
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_activities(db, pagination.offset, pagination.limit)
