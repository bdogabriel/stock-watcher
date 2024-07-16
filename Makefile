all: stockwatcher/manage.py
	python3 stockwatcher/manage.py runserver

migrations:
	python3 stockwatcher/manage.py makemigrations

migrate:
	python3 stockwatcher/manage.py migrate

requirements:
	pip freeze > stockwatcher/requirements.txt

docker-compose:
	docker-compose up -d --build