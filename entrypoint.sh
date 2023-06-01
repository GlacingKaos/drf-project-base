#!/bin/bash
set -eu
set -o pipefail

python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput

exec "$@"
