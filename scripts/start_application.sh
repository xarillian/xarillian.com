#!/bin/bash
set -e

cd /home/ubuntu/xarillian.com

source venv/bin/activate

mkdir -p logs

gunicorn --bind 127.0.0.1:8000 wsgi:app \
  --daemon \
  --pid gunicorn.pid \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log

deactivate