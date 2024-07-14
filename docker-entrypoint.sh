#!/bin/sh

python manage.py migrate
python -m pysassc younhalibrary/scss/main.scss younhalibrary/static/main.css -s compressed
python manage.py collectstatic --no-input --clear

exec "$@"
