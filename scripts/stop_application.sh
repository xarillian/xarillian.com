#!/bin/bash
set -e

cd /home/ubuntu/xarillian.com

if [ -f gunicorn.pid ]; then
    kill $(cat gunicorn.pid) || true
    rm gunicorn.pid
else
    echo "No gunicorn.pid file found. Gunicorn may not be running."
fi
