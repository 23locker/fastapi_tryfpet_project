# fastapi_pet_project

пет-проект для разных экспериментов с fastapi

## технологии

- **fastapi** — web фреймворк
- **sqlalchemy** — orm для работы с бд
- **postgresql** — база данных
- **asyncpg** — асинхронный драйвер для postgres
- **pydantic** — валидация данных
- **uv** — пакетный менеджер и инструмент для управления окружением
- **docker compose** — контейнеризация бд

## быстрый старт

### 1. установка зависимостей

```bash
uv sync
```

### 2. запуск базы данных

```bash
docker compose up -d
```

### 3. создание `.env` файла

```env
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
```

### 4. запуск сервера

```bash
uv run main.py
```

сервер доступен на `http://localhost:8000`

## структура проекта

```
в разработке...
```

## todo

- [ ] разделить `main.py` на модули (routes, models, dao, schemas)
- [ ] добавить alembic миграции для бд
- [ ] покрыть тесты (pytest)
- [ ] добавить логирование
- [ ] настроить линтинг (ruff, black)
- [ ] добавить валидацию ошибок во все ручки
- [ ] документация api (swagger уже работает на `/docs`)
- [ ] кэширование
- [ ] rate limiting
