#!/bin/bash
source /home/ubuntu/xarillian.com/venv/bin/activate
cd /home/ubuntu/xarillian.com
gunicorn --bind 0.0.0.0:8000 app:app --daemon