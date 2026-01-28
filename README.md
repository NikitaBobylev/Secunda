# Secunda Directory API

REST API для справочника организаций, зданий и видов деятельности.

## Быстрый старт (uv)
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.seed
uvicorn main:app --reload
```

## Переменные окружения
- `SECUNDA_API_KEY` — статический API ключ (по умолчанию `changeme`).
- `SECUNDA_DATABASE_URL` — строка подключения (по умолчанию `sqlite:///./secunda.db`).
- `SECUNDA_ASYNC_DATABASE_URL` — опционально, async строка подключения.

## Авторизация
Все запросы требуют заголовок:
```
X-API-Key: <ваш_ключ>
```

## Основные эндпоинты
- `GET /api/v1/buildings/?offset=0&limit=100` — список зданий.
- `POST /api/v1/buildings/` — создание здания (валидируются координаты).
- `GET /api/v1/activities/?offset=0&limit=100` — список видов деятельности.
- `GET /api/v1/organizations/by-id/{id}` — организация по идентификатору.
- `GET /api/v1/organizations/by-building/{building_id}?offset=0&limit=100` — организации в здании.
- `GET /api/v1/organizations/by-activity/{activity_id}?include_descendants=true&offset=0&limit=100` — организации по виду деятельности (с учетом вложенных по умолчанию).
- `GET /api/v1/organizations/search?name=...&activity_id=...&offset=0&limit=100` — поиск организаций по названию и/или виду деятельности (по ID).
- `GET /api/v1/organizations/search-by-activity?activity_name=...&offset=0&limit=100` — поиск организаций по виду деятельности по названию с учетом вложенности.
- `GET /api/v1/organizations/within-radius?latitude=...&longitude=...&radius_km=...&offset=0&limit=100` — организации в радиусе.
- `GET /api/v1/organizations/within-box?lat_min=...&lat_max=...&lon_min=...&lon_max=...&offset=0&limit=100` — организации в прямоугольной области.

Все list-эндпоинты возвращают структуру:
```json
{
  "items": [],
  "offset": 0,
  "limit": 100,
  "total": 0
}
```

## Документация API
- Swagger UI: `/docs`
- Redoc: `/redoc`

## Docker
```bash
docker compose up --build
```

Перед первым запуском внутри контейнера можно выполнить миграции и сиды:
```bash
docker compose run --rm api alembic upgrade head
docker compose run --rm api python -m app.seed
```

После запуска доступ по адресу `http://localhost/` (Nginx).
