#!/bin/bash

python manage.py collectstatic --no-input

exec gunicorn --bind 0.0.0.0:8000 --workers 3 tc4a.wsgi:application

