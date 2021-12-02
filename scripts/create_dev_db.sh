#!/usr/bin/env sh

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT_DIR="$( realpath ${SCRIPT_DIR}/.. )"

DB_FILE="${REPO_ROOT_DIR}/db.sqlite3"

SU_DEFAULT_NAME="daniel"
SU_DEFAULT_EMAIL="daniel.nitsche@astro.su.se"

if [ -f "${DB_FILE}" ]; then
  read -p "Database ${DB_FILE} already exists. Delete it (y/N)? " remove
  if [ "${remove}" == "y" ]; then
    rm -f "${DB_FILE}"
  fi
fi

./manage.py makemigrations
./manage.py migrate
./manage.py createcachetable

echo "Adding super user to database"
./manage.py createsuperuser --username "${SU_DEFAULT_NAME}" --email "${SU_DEFAULT_EMAIL}"
