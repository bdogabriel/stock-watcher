#!/bin/ash

echo "Apply database migrations"
python3 manage.py makemigrations
python3 manage.py migrate

exec "$@"