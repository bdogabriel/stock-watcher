all:
	python3 src/manage.py runserver

celery:
	celery --workdir=src -A stockwatcher worker --beat -l INFO

migrations:
	python3 src/manage.py makemigrations

migrate:
	python3 src/manage.py migrate

requirements:
	pip freeze > requirements.txt

docker:
	docker compose build --no-cache
	docker compose up -d 

docker-start:
	docker container start postgres redis django celery

docker-django-shell:
	docker exec -it django /bin/sh

docker-stop:
	docker container stop celery django redis postgres

docker-clear: docker-stop
	docker rm django celery redis postgres
	docker rmi stock-watcher-django stock-watcher-celery
	docker volume prune -af

rebuild: docker-clear docker