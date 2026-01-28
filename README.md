# Secunda Directory API

REST API для справочника организаций, зданий и видов деятельности.

## Быстрый старт (uv)
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
mkdir -p data logs
alembic upgrade head
python -m app.seed
uvicorn main:app --reload
```

## Переменные окружения
- `SECUNDA_API_KEY` — статический API ключ (по умолчанию `changeme`).
- `SECUNDA_DATABASE_URL` — строка подключения (по умолчанию `sqlite:///./data/secunda.db`).
- `SECUNDA_ASYNC_DATABASE_URL` — опционально, async строка подключения.
- `SECUNDA_LOG_PATH` — путь к файлу логов (по умолчанию `logs/app.log`).

## Авторизация
Все запросы требуют заголовок:
```
X-API-Key: <ваш_ключ>
```

## Основные эндпоинты
- `GET /api/v1/buildings/?offset=0&limit=100` — список зданий.
- `GET /api/v1/activities/?offset=0&limit=100` — список видов деятельности.
- `GET /api/v1/organizations/by-id/{id}` — организация по идентификатору.
- `GET /api/v1/organizations/search?name=...&activity_id=...&offset=0&limit=100` — поиск организаций по названию и/или виду деятельности и/или по зданию (по ID).
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

При старте контейнера автоматически выполняются миграции и сиды.

После запуска доступ по адресу `http://localhost/` (Nginx).

## Локальный запуск без Docker
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
mkdir -p data logs
alembic upgrade head
python -m app.seed
uvicorn main:app --reload
```

Проверь `.env` для локального запуска:
- `SECUNDA_DATABASE_URL=sqlite:///./data/secunda.db`
- `SECUNDA_LOG_PATH=logs/app.log`
