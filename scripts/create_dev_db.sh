#!/usr/bin/env sh

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

DB_FILE="${ROOT_DIR}/db.sqlite3"

SU_DEFAULT_NAME="daniel"
SU_DEFAULT_EMAIL="daniel.nitsche@astro.su.se"

. "${ROOT_DIR}/venv/bin/activate"

if [ -f "${DB_FILE}" ]; then
  read -p "Database ${DB_FILE} already exists. Delete it (y/N)? " remove
  if [ "${remove}" == "y" ]; then
    rm -f "${DB_FILE}"
  fi
fi

"${ROOT_DIR}/manage.py" makemigrations
"${ROOT_DIR}/manage.py" migrate
"${ROOT_DIR}/manage.py" createcachetable

echo "Adding super user to database"
"${ROOT_DIR}/manage.py" createsuperuser --username "${SU_DEFAULT_NAME}" --email "${SU_DEFAULT_EMAIL}"

deactivate
