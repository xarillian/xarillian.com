#!/bin/bash
set -e

cd /home/ubuntu/xarillian.com

source venv/bin/activate

pkill gunicorn || true
gunicorn --bind 127.0.0.1:8000 app:app --daemon

deactivate