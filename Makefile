.PHONY: up down build restart logs shell test migrate makemigrations

# Запуск
up:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down

restart:
	docker compose restart app

logs:
	docker compose logs -f app

# База данных
migrate:
	docker compose run --rm app alembic upgrade head

makemigrations:
	docker compose run --rm app alembic revision --autogenerate -m "$(name)"

downgrade:
	docker compose run --rm app alembic downgrade -1

# Тесты
test:
	docker compose run --rm app pytest -v

test-cov:
	docker compose run --rm app pytest -v --cov=app --cov-report=term-missing

# Утилиты
shell:
	docker compose exec app bash
