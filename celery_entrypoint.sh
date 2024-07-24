#!/bin/sh

set -e

while ! nc -z django 8000; do
  echo -e "\t🟡\tWaiting for Django Startup (django:8000) ..."
  sleep 2
done

echo -e "\t✅\tDjango Started Successfully (django:8000)"

celery -A stockwatcher worker --beat -l INFO