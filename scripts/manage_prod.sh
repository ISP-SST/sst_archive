#!/usr/bin/env sh

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

. "${ROOT_DIR}/venv/bin/activate"

if [[ "$1" == "--help" ]] || [ -z "$@"]; then
  "${ROOT_DIR}/manage.py" "$@"
else
  "${ROOT_DIR}/manage.py" "$@" --settings sst_archive.settings.prod
fi

deactivate
