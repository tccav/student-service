.PHONY: build-app-image
build:
	docker build -t student_service_image .

.PHONY: migrate-up
migrate-up:
	dbmate -u "postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?${DB_OPTIONS}" up

.PHONY: migrate-down
migrate-down:
	dbmate -u "postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?${DB_OPTIONS}" down

.PHONY: start-composer
start-composer:
	docker compose -f docker-compose.yml up

.PHONY: stop-composer
stop-composer:
	docker compose -f docker-compose.yml down

