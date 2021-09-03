#!/usr/bin/env sh

rm -f db.sqlite3
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser --username daniel --email daniel.nitsche@astro.su.se
