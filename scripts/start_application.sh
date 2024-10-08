#!/bin/bash
set -e

cd /home/ubuntu/xarillian.com

source venv/bin/activate

gunicorn --bind 0.0.0.0:8000 app:app --daemon

echo "Running processes:"
ps aux | grep gunicorn

deactivate