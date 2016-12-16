#!/bin/bash

python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput

/usr/local/bin/gunicorn --reload hackathon.wsgi:application -w 2 -b :8000
