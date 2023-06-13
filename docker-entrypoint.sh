#!/bin/sh

echo "Waiting for postgres..."

until echo "select 1;" | python manage.py dbshell > /dev/null 2>&1; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py loaddata medialib_live_data
python -m pysassc younhalibrary/scss/main.scss younhalibrary/static/main.css -s compressed

exec "$@"
