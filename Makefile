.PHONY: build start stop

build:
	@if [[ ! -f ".env" || ! -f ".db-env" || ! -f app/.envv ]]; \
		then echo "ERROR! .env, .db-env or app/.env missing"; \
		exit 1; \
	fi
	@docker-compose build
	@docker-compose run --rm app python ./manage.py collectstatic --no-input

start:
	@docker-compose up -d

stop:
	@docker-compose stop
