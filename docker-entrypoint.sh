#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input --clear
python -m pysassc younhalibrary/scss/main.scss younhalibrary/static/main.css -s compressed

exec "$@"
