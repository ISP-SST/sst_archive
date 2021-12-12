#!/usr/bin/env sh

. ./venv/bin/activate
./manage.py "$@" --settings sst_archive.settings.prod
deactivate
