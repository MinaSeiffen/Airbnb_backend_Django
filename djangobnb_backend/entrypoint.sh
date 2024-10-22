#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Check if database is ready..."
  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done
  echo "Database is ready!"
fi

python manage.py migrate

exec "$@"