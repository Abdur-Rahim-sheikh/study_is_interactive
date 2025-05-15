run:
	docker compose up --build 

clear:
	docker compose down --remove-orphans

start:
	docker compose up

watch:
	docker compose up --build --watch