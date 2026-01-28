import logging
from collections import deque

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.activity import ActivityRepository
from app.schemas.pagination import PaginatedResponse

logger = logging.getLogger(__name__)


def _descendant_ids(root_ids: list[int], activities) -> list[int]:
    by_parent: dict[int | None, list] = {}
    for activity in activities:
        by_parent.setdefault(activity.parent_id, []).append(activity)

    result: set[int] = set()
    queue: deque[int] = deque(root_ids)
    while queue:
        current_id = queue.popleft()
        if current_id in result:
            continue
        result.add(current_id)
        for child in by_parent.get(current_id, []):
            queue.append(child.id)
    return list(result)


class ActivityService:
    def __init__(self, repo: ActivityRepository | None = None) -> None:
        self.repo = repo or ActivityRepository()

    async def list_activities(
        self, db: AsyncSession, offset: int, limit: int
    ) -> PaginatedResponse:
        items, total = await self.repo.list_items(db, offset, limit)
        return PaginatedResponse(items=items, offset=offset, limit=limit, total=total)

    async def get_descendant_ids(self, db: AsyncSession, activity_id: int) -> list[int]:
        activities = await self.repo.list_all(db)
        if not any(activity.id == activity_id for activity in activities):
            return []
        return _descendant_ids([activity_id], activities)

    async def get_descendant_ids_by_name(
        self, db: AsyncSession, name: str
    ) -> list[int]:
        activities = await self.repo.list_all(db)
        needle = name.casefold()
        root_ids = [activity.id for activity in activities if activity.name.casefold() == needle]
        if not root_ids:
            return []
        return _descendant_ids(root_ids, activities)
