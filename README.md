# AI Content Moderation Platform

SaaS API платформа для асинхронной модерации пользовательского контента с использованием AI.

## Технологии

- **FastAPI** — async REST API
- **PostgreSQL** + **SQLAlchemy** (async) — база данных
- **Alembic** — миграции схемы БД
- **Redis** — брокер задач и кэш
- **Celery** — асинхронная обработка AI запросов
- **Docker** + **Docker Compose** — контейнеризация
- **pytest** — unit и integration тесты
- **OpenAI API** — AI модерация контента

## Архитектура

Client → FastAPI → PostgreSQL
↓
Redis (broker)
↓
Celery Worker → OpenAI API
↓
PostgreSQL (результат)


## Быстрый старт

**1. Клонировать репозиторий:**
```bash
git clone https://github.com/<your-username>/ai-content-moderator
cd ai-content-moderator
```

**2. Создать `.env` файл:**
```bash
cp .env.example .env
# Заполнить значения в .env
```

**3. Запустить:**
```bash
make build
make migrate
```

**4. Открыть документацию:**

[http://localhost:8000/docs](http://localhost:8000/docs)

## Использование API

**Регистрация компании:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My Company", "email": "admin@company.com", "password": "secret"}'
```

**Получение JWT токена:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "secret"}'
```

**Создание API ключа:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/api-keys \
  -H "Authorization: Bearer <jwt_token>"
```

**Отправка контента на модерацию:**
```bash
curl -X POST http://localhost:8000/api/v1/moderate/ \
  -H "x-api-key: <api_key>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Text to moderate", "content_type": "text"}'
```

**Получение результата:**
```bash
curl http://localhost:8000/api/v1/moderate/<request_id> \
  -H "x-api-key: <api_key>"
```

## Команды

```bash
make up           # Запустить все сервисы
make build        # Пересобрать и запустить
make down         # Остановить все сервисы
make migrate      # Применить миграции
make test         # Запустить тесты
make test-cov     # Тесты с отчётом покрытия
make logs         # Логи приложения
make shell        # Войти в контейнер
```

## Тесты

```bash
make test
```

Покрытие кода: ~77%
