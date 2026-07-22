.PHONY: test create-requirements ruff-check ruff-fix coverage setup start up

start: setup create-requirements up

test:
	cd api && ENVIRONMENT=test poetry run pytest

create-requirements:
	cd api && poetry export -f requirements.txt --without-hashes --output config/requirements.txt

up:
	docker compose -f 'docker-compose.yml' up -d --build

ruff-check:
	cd api && poetry run ruff check .

ruff-fix:
	cd api && poetry run ruff check . --fix

coverage:
	cd api && ENVIRONMENT=test poetry run coverage run -m pytest

setup:
	cp -n api/config/.env-example .env || echo ".env already exists"
