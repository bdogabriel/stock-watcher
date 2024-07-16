all: stockwatcher/manage.py
	python3 stockwatcher/manage.py runserver

migrations:
	python3 stockwatcher/manage.py makemigrations

migrate:
	python3 stockwatcher/manage.py migrate

requirements:
	pip freeze > stockwatcher/requirements.txt

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
	docker rmi redis:7.0.11-alpine stock-watcher-django stock-watcher-celery