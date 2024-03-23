#!/bin/sh
echo "------------Starting migration------------"
python3 manage.py makemigrations && echo "Migrations done" &&

echo "----------------Migrating-----------------"
python3 manage.py migrate && echo "Migrate done" &&

echo "-------------Starting server--------------"
gunicorn mail_app_be.wsgi:application --bind 0.0.0.0:8000