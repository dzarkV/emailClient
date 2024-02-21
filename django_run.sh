#!/bin/sh
echo "------------Starting migration------------"
python3 manage.py makemigrations && echo "Migrations done" &&

echo "----------------Migrating-----------------"
python3 manage.py migrate && echo "Migrate done" &&

echo "-------------Starting server--------------"
python3 manage.py runserver 0.0.0.0:8000