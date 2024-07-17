all: src/manage.py
	python3 src/manage.py runserver

migrations:
	python3 src/manage.py makemigrations

migrate: migrations
	python3 src/manage.py migrate

requirements:
	pip freeze > src/requirements.txt

docker:
	docker-compose up -d --build

docker-start:
	docker container start redis django celery

docker-django-shell:
	docker exec -it django /bin/sh

docker-stop:
	docker container stop django celery redis

docker-clear: docker-stop
	docker rm django celery redis
	docker rmi redis stock-watcher-django stock-watcher-celery
	docker volume rm stock-watcher-volume stock-watcher-redis-data-volume

rebuild: docker-clear docker