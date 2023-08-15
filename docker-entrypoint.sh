#!/bin/sh
set -e
set -u

if [ -n "${MODE}" ] && [ "${MODE}" != "dev" ]; then
  uwsgi --http 0.0.0.0:8000 --master -p 4 -w wsgi:app
else
  flask run
fi
