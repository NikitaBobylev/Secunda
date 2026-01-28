from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import api_key_auth
from app.db.session import get_db
from app.schemas.organization import OrganizationOut
from app.schemas.pagination import PaginatedResponse, PaginationParams, pagination_params
from app.services.organizations import OrganizationService

router = APIRouter(dependencies=[Depends(api_key_auth)])
service = OrganizationService()


@router.get("/by-id/{organization_id}", response_model=OrganizationOut)
async def get_organization(organization_id: int, db: AsyncSession = Depends(get_db)):
    organization = await service.get_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return organization


# @router.get(
#     "/by-building/{building_id}", response_model=PaginatedResponse[OrganizationOut]
# )
# async def list_by_building(
#     building_id: int,
#     pagination: PaginationParams = Depends(pagination_params),
#     db: AsyncSession = Depends(get_db),
# ):
#     return await service.list_by_building(
#         db, building_id, pagination.offset, pagination.limit
#     )


# @router.get(
#     "/by-activity/{activity_id}", response_model=PaginatedResponse[OrganizationOut]
# )
# async def list_by_activity(
#     activity_id: int,
#     include_descendants: bool = Query(True),
#     pagination: PaginationParams = Depends(pagination_params),
#     db: AsyncSession = Depends(get_db),
# ):
#     return await service.list_by_activity(
#         db, activity_id, include_descendants, pagination.offset, pagination.limit
#     )


@router.get("/search", response_model=PaginatedResponse[OrganizationOut])
async def filter_search(
    name: str | None = Query(None),
    activity_id: int | None = Query(None),
    building_id: int | None = Query(None),
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    return await service.search(
        db=db, name=name,
        activity_id=activity_id,
        building_id=building_id,
        offset=pagination.offset, 
        limit=pagination.limit
    )


@router.get(
    "/search-by-activity-name", response_model=PaginatedResponse[OrganizationOut]
)
async def search_by_activity_name(
    activity_name: str = Query(..., min_length=1),
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    return await service.search_by_activity_name(
        db, activity_name, pagination.offset, pagination.limit
    )


@router.get("/within-radius", response_model=PaginatedResponse[OrganizationOut])
async def list_within_radius(
    latitude: float,
    longitude: float,
    radius_km: float = Query(..., gt=0),
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_within_radius(
        db, latitude, longitude, radius_km, pagination.offset, pagination.limit
    )


@router.get("/within-box", response_model=PaginatedResponse[OrganizationOut])
async def list_within_box(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    pagination: PaginationParams = Depends(pagination_params),
    db: AsyncSession = Depends(get_db),
):
    if lat_min > lat_max or lon_min > lon_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bounding box",
        )
    return await service.list_within_box(
        db, lat_min, lat_max, lon_min, lon_max, pagination.offset, pagination.limit
    )
