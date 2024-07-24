FROM python:3.10.12-alpine

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
COPY entrypoint.sh /usr/src/entrypoint.sh
COPY celery_entrypoint.sh /usr/src/celery_entrypoint.sh

WORKDIR /usr/src/app

RUN  pip install --upgrade pip && pip install -r requirements.txt &&  adduser --disabled-password --no-create-home duser && chmod +x /usr/src/entrypoint.sh && chmod +x /usr/src/celery_entrypoint.sh

USER duser