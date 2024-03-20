#!/bin/bash
python manage.py collectstatic

python3 manage.py migrate
python3 manage.py loaddata db.json
gunicorn admin_panel_for_bot.wsgi:application --bind 0.0.0.0:8000 --workers 3
